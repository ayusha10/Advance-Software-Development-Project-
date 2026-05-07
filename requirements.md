# Horizon Cinemas Requirements

Checked against the current workspace state on 2026-05-07.

Validation run:
- `py run_tests.py` passed with 41/41 tests.
- Workspace error scan reported no syntax or compile errors.

## Implemented

- Role-based login routing exists for Admin, Manager, Customer, and Booking-Staff in [gui/loginWindow.py](gui/loginWindow.py#L80).
- Booking creation enforces the 7-day advance window, seat availability checks, and unique booking references in [app/services/booking_service.py](app/services/booking_service.py#L49).
- Booking receipts include booking reference, film name, booking date, show time, screen number, ticket count, seat numbers, and total price in [app/services/booking_service.py](app/services/booking_service.py#L147).
- Seat-class pricing is implemented for lower, upper, and VIP seats in [app/models/show.py](app/models/show.py#L50).
- Pricing now also varies by city and time of day in [app/models/show.py](app/models/show.py#L1).
- Seat generation for new screens now splits seats into lower, upper, and VIP sections in [app/repositories/screen_repository.py](app/repositories/screen_repository.py#L48).
- Booking-staff bookings now require an assigned city and are constrained by that city in [app/services/booking_service.py](app/services/booking_service.py#L49).
- Cancellation blocks same-day cancellations and applies a 50% refund for allowed cancellations in [app/services/booking_service.py](app/services/booking_service.py#L161).
- A dedicated cancellation window exists in [gui/cancellation_gui.py](gui/cancellation_gui.py).
- Admin reports are implemented in [app/controllers/admin_controller.py](app/controllers/admin_controller.py#L169).
- Managers can reach the full admin dashboard and also switch to a manager view from [gui/admin_panal.py](gui/admin_panal.py#L26).
- Cinema and show management are no longer limited to a single assigned city in [gui/manager_panal.py](gui/manager_panal.py#L1).
- Film listings now show descriptions, actors, and show times in [gui/customer_panel.py](gui/customer_panel.py#L1) and [gui/admin_panal.py](gui/admin_panal.py#L1).
- Booking forms now include an explicit seat-type selector in [gui/customer_panel.py](gui/customer_panel.py#L1) and [gui/booking_staff_panel.py](gui/booking_staff_panel.py#L1).

## Status

- No known structural data gaps remain in the seeded database.
- The cancellation flow is implemented as a dedicated window with booking lookup and cancellation actions.

## Data Snapshot

The current `horizon_db.sqlite3` snapshot matches the target structure:

- 4 cities exist: Birmingham, Bristol, Cardiff, and London.
- 8 cinemas exist, which gives 2 cinemas per city.
- 12 screens exist, and every screen is now seeded with 70 seats.
- Every seeded screen has 1-2 shows, so the 1-3 daily show coverage is demonstrated across the dataset.
- Booking-staff seed users are assigned to city 1 in the current database.

## Bottom Line

The core booking, cancellation, listing, pricing, role-access, and seeded data requirements are satisfied in the current workspace state.
