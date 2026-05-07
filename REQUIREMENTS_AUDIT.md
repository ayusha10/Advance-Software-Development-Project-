# Horizon Cinemas Requirements Audit

Checked against the current workspace state on 2026-05-07.

Validation run:
- `py run_tests.py` completed successfully with 41/41 tests passing.
- Workspace error scan reported no syntax or compile errors.

## Implemented Correctly

- Role-based login routing exists for Admin, Manager, Customer, and Booking-Staff in [gui/loginWindow.py](gui/loginWindow.py#L80).
- Booking creation enforces a 7-day advance window, seat availability checks, and unique booking references in [app/services/booking_service.py](app/services/booking_service.py#L49).
- Booking receipts include booking reference, film name, booking date, show time, screen number, ticket count, seat numbers, and total price in [app/services/booking_service.py](app/services/booking_service.py#L147).
- Seat-class pricing is implemented for lower, upper, and VIP seats in [app/models/show.py](app/models/show.py#L50).
- Pricing now also varies by city and time of day in [app/models/show.py](app/models/show.py#L1).
- Seat generation for new screens now splits seats into lower, upper, and VIP sections in [app/repositories/screen_repository.py](app/repositories/screen_repository.py#L48).
- Booking-staff bookings now require an assigned city and are constrained by that city in [app/services/booking_service.py](app/services/booking_service.py#L49).
- Cancellation now blocks same-day cancellations and applies a 50% refund for allowed cancellations in [app/services/booking_service.py](app/services/booking_service.py#L161).
- Admin reports are implemented in the controller layer, including booking counts, revenue, top film, and staff booking totals in [app/controllers/admin_controller.py](app/controllers/admin_controller.py#L169).
- Managers can now reach the full admin dashboard and also switch to a manager view from [gui/admin_panal.py](gui/admin_panal.py#L26).
- Cinema and show management are no longer limited to a single assigned city in the manager panel, so managers can work across the full dataset in [gui/manager_panal.py](gui/manager_panal.py#L1).
- Film listings now show descriptions, actors, and show times in [gui/customer_panel.py](gui/customer_panel.py#L1) and [gui/admin_panal.py](gui/admin_panal.py#L1).
- Booking forms now include an explicit seat-type selector in [gui/customer_panel.py](gui/customer_panel.py#L1) and [gui/booking_staff_panel.py](gui/booking_staff_panel.py#L1).

## Remaining Gaps

- A dedicated standalone cancellation GUI is still not present; cancellation is embedded inside the booking, customer, and staff booking views.
- The show schedule is denser than before, but the seeded database still does not demonstrate the full target coverage for every screen.

## Not Implemented Yet

- None of the currently verified requirement gaps are blocking core booking, listing, or role access.

## Current Data Snapshot

The current `horizon_db.sqlite3` snapshot is closer to the structural target than the initial SQL file, but it still has a few mismatches:

- 4 cities exist.
- 8 cinemas exist, which gives 2 cinemas per city.
- 12 screens exist, so the "up to 6 screens per cinema" requirement is satisfied.
- 1 screen has only 20 seats, which is below the requested 50-120 seat range.
- The show schedule is sparse and does not clearly demonstrate 1-3 daily shows per screen.
- Booking-staff seed users are assigned to city 1 in the current database, which is good for city filtering, but only one city is represented in that role assignment.

## Bottom Line

There are no hard runtime or syntax errors reported by the automated checks. The main remaining gap is the absence of a separate cancellation-only GUI.