from django.db import transaction
from django.db.models import Sum, F, Q
from django.conf import settings
from celery import shared_task
from railways.models import Bookings, Train

@shared_task(queue=settings.BOOKING_PROCESSING_QUEUE)
def process_booking_information(data):
    train_id = data.get("train")
    source = data.get("source")
    destination = data.get("destination")
    seats = data.get("seats")
    booking_id = data.get("id")

    user_id = data.get("user_id")

    # We prevent races to book tickets by locking the booking rows
    # first, and then checking the availabilty, confirming the booking
    # and then unlocking it.
    with transaction.atomic():
        booking = Bookings.objects.select_for_update().get(id=booking_id)

        is_seats_available = check_seat_availability(train_id, source, destination, seats)
        
        if is_seats_available:
            booking.status = Bookings.CONFIRMED
        else:
            booking.status = Bookings.CANCELLED

        booking.save()



# This verifies the availability of seats from
# the database for a given train.
#
# This is a costly operation, hence we resort
# to it only before processing a transaction. 
def check_seat_availability(
    train_id,
    source,
    destination,
    seats
):
    total_seats = Train.objects.filter(id=train_id).values_list("seats", flat=True).first()

    if total_seats is None:
        return False
    
    # We first aggregate all the booked seats between point A
    # and B such that the source or destination is between point
    # A and B.
    #
    # This allows us to estimate available seats for entirity of
    # the journey.
    booked_seats = Bookings.objects.filter(
        Q(train_id=train_id, status=Bookings.CONFIRMED, source__gte=source, source__lte=destination) |
        Q(train_id=train_id, status=Bookings.CONFIRMED, destination__gte=source, destination__lte=destination)
    ).aggregate(
        booked = Sum("seats")
    )

    # If we don't find anything seats that matches our
    # criteria in Bookings, that means there are None.
    if booked_seats.get("booked") is None:
        booked_seats["booked"] = 0

    if total_seats - booked_seats.get("booked") < seats:
        return False
    
    return True



