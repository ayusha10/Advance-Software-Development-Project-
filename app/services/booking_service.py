import uuid
from datetime import datetime, date, timedelta
from config.database import get_connection
from app.repositories.show_repository import ShowRepository
from app.repositories.seat_repository import SeatRepository
from app.repositories.booking_repository import BookingRepository


class BookingError(Exception):
    pass


class BookingService:
    def __init__(self):
        self.show_repo = ShowRepository()
        self.seat_repo = SeatRepository()
        self.booking_repo = BookingRepository()

    def _generate_booking_ref(self):
        # Human-friendly unique reference
        return f"HC-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"

    def _get_promo(self, promo_code):
        if not promo_code:
            return None
        conn = get_connection()
        conn.row_factory = __import__('sqlite3').Row
        cur = conn.cursor()
        today = date.today().isoformat()
        cur.execute("SELECT * FROM promotions WHERE promo_code = ? AND is_active = 1 AND valid_from <= ? AND valid_to >= ?", (promo_code, today, today))
        promo = cur.fetchone()
        cur.close()
        conn.close()
        return None if not promo else dict(promo)

    def get_available_seats_for_show(self, show_id):
        """Get all seats not booked or locked for this show"""
        booked_rows = self.booking_repo.get_booked_seats_for_show(show_id)
        booked_seat_ids = {r['seat_id'] for r in booked_rows}
        
        locked_rows = self.booking_repo.get_locked_seats_for_show(show_id)
        locked_seat_ids = {r[0] for r in locked_rows}  # seat_id is first column
        
        unavailable_ids = booked_seat_ids | locked_seat_ids
        
        all_seats = self.seat_repo.get_all_seats()
        return [s for s in all_seats if s.get_id() not in unavailable_ids]

    def create_booking(self, user, show_id, seat_ids, customer_user_id=None, promo_code=None):
        # De-duplicate in case UI sends the same seat twice.
        seat_ids = list(dict.fromkeys(seat_ids))
        # Role checks
        # Booking staff must create bookings on behalf of a customer (cannot book for themselves)
        if getattr(user, 'role', None) == 'Booking-Staff' and not customer_user_id:
            raise BookingError('Booking staff must create bookings on behalf of a customer')

        if getattr(user, 'role', None) == 'Booking-Staff' and not getattr(user, 'assigned_city_id', None):
            raise BookingError('Booking staff must have an assigned city')

        # Only Admin, Manager or Booking-Staff may create bookings on behalf of customers
        if customer_user_id and getattr(user, 'role', None) not in ('Admin', 'Manager', 'Booking-Staff'):
            raise BookingError('Only Admin, Manager or Booking-Staff can create bookings on behalf of customers')

        show = self.show_repo.get_show_by_id(show_id)
        if not show:
            raise BookingError('Show not found')

        # Enforce booking window (up to 7 days in advance)
        show_date = datetime.strptime(show.show_date, '%Y-%m-%d').date()
        today = date.today()
        if show_date < today or show_date > (today + timedelta(days=7)):
            raise BookingError('Bookings allowed only for shows from today up to 7 days in advance')

        # Booking staff restrictions: can only book within assigned city
        if getattr(user, 'role', None) == 'Booking-Staff' and getattr(user, 'assigned_city_id', None):
            # get show's city id
            conn = get_connection()
            conn.row_factory = __import__('sqlite3').Row
            cur = conn.cursor()
            cur.execute("SELECT c.city_id FROM shows s JOIN screens sc ON s.screen_id = sc.id JOIN cinemas c ON sc.cinema_id = c.id WHERE s.id = ?", (show_id,))
            row = cur.fetchone()
            cur.close()
            conn.close()
            if row and row['city_id'] != user.assigned_city_id:
                raise BookingError('Booking staff can only book shows in their assigned city')

        # Check seat availability
        booked_rows = self.booking_repo.get_booked_seats_for_show(show_id)
        booked_seat_ids = {r['seat_id'] for r in booked_rows}

        seats = []
        for sid in seat_ids:
            s = self.seat_repo.get_seat_by_id(sid)
            if not s:
                raise BookingError(f'Seat id {sid} not found')
            if s.id in booked_seat_ids:
                raise BookingError(f'Seat {s.get_seat_number()} already booked for this show')
            seats.append(s)

        # Compute price
        tickets_total = 0.0
        for s in seats:
            st = s.get_seat_type().lower()
            if st == 'lower':
                pt = show.price_for('lower', vip=False)
            elif st == 'upper':
                pt = show.price_for('upper', vip=False)
            elif st == 'vip':
                # VIP seats are treated as upper + vip flag
                pt = show.price_for('upper', vip=True)
            else:
                pt = show.price_for('upper', vip=False)
            tickets_total += float(pt)

        promo = self._get_promo(promo_code)
        discount = 0.0
        if promo:
            discount = (promo['discount_percentage'] / 100.0) * tickets_total

        service_fee = 5.00
        subtotal = tickets_total - discount
        total_price = round(subtotal + service_fee, 2)

        # Generate booking
        booking_ref = self._generate_booking_ref()
        booking_user_id = customer_user_id if customer_user_id else getattr(user, 'user_id', None)
        if not booking_user_id:
            raise BookingError('No booking user specified')

        # Create booking record
        import app.models.booking as booking_model
        b = booking_model.Booking(
            id=None,
            booking_ref=booking_ref,
            user_id=booking_user_id,
            show_id=show_id,
            promo_id=(promo['id'] if promo else None),
            total_price=total_price,
            service_fee=service_fee,
            status='CONFIRMED',
            booking_date=show.show_date,
            created_at=None
        )
        booking_id = self.booking_repo.add_booking(b)

        # Persist booked seats
        for s in seats:
            self.booking_repo.add_booked_seat(booking_id, show_id, s.get_id())

        # Return receipt
        receipt = {
            'booking_ref': booking_ref,
            'film_name': show.film_name,
            'film_date': show.show_date,
            'booking_date': show.show_date,
            'show_time': show.show_time,
            'screen_number': show.screen_number,
            'number_of_tickets': len(seats),
            'seat_numbers': [s.get_seat_number() for s in seats],
            'total_price': total_price,
            'created_at': datetime.utcnow().isoformat()
        }
        return receipt

    def cancel_booking(self, user, booking_ref, reason=None):
        # Only Manager, Admin, Booking-Staff or the user who made the booking can cancel
        booking = self.booking_repo.get_booking_by_ref(booking_ref)
        if not booking:
            raise BookingError('Booking not found')

        # Fetch show to check date
        show = self.show_repo.get_show_by_id(booking.get_show_id())
        if not show:
            raise BookingError('Associated show not found')

        show_date = datetime.strptime(show.show_date, '%Y-%m-%d').date()
        today = date.today()
        days_before_show = (show_date - today).days

        # No cancellation/refund for missed shows.
        if days_before_show < 0:
            raise BookingError('Cancellation not allowed after the show date')

        if days_before_show == 0:
            raise BookingError('Cancellation not allowed on the day of the show')

        # Permission check
        allowed_roles = ('Admin', 'Manager', 'Booking-Staff')
        if getattr(user, 'role', None) not in allowed_roles and getattr(user, 'user_id', None) != booking.get_user_id():
            raise BookingError('Not authorized to cancel this booking')

        # Refund policy:
        # - More than 1 day before show: full refund
        # - Exactly 1 day before show: 50% refund
        if days_before_show > 1:
            refund_amount = round(float(booking.get_total_price()), 2)
        else:
            refund_amount = round(float(booking.get_total_price()) * 0.5, 2)

        # Update booking status
        self.booking_repo.cancel_booking(booking_ref)

        # Release seat locks for this booking so seats can be booked again.
        self.booking_repo.delete_booked_seats_by_booking(booking.get_id())

        # Insert into cancellations table
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO cancellations (booking_id, reason, refund_amount) VALUES (?, ?, ?)", (booking.get_id(), reason, refund_amount))
        conn.commit()
        cur.close()
        conn.close()

        return {'booking_ref': booking_ref, 'refund_amount': refund_amount}

    def lock_seats(self, show_id, seat_ids):
        """Lock seats for booking process (temporary reservation)"""
        self.booking_repo.cleanup_expired_locks(timeout_minutes=10)
        locked = []
        for seat_id in seat_ids:
            if self.booking_repo.lock_seat(show_id, seat_id):
                locked.append(seat_id)
        return locked

    def unlock_seats(self, show_id, seat_ids):
        """Release seat locks after booking complete or cancelled"""
        for seat_id in seat_ids:
            self.booking_repo.unlock_seat(show_id, seat_id)

    def get_seat_lock_status(self, show_id):
        """Check which seats are currently locked for a show"""
        return self.booking_repo.get_locked_seats_for_show(show_id)
