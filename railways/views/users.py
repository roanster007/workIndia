from django.http import JsonResponse
from django.views import View
from railways.lib.users import (
    maybe_register_user,
    maybe_get_booking_details,
    maybe_process_booking,
    maybe_get_available_seats,
    login_user,
)


class Register(View):
    # Used to register a user
    def post(self, request):
        email = request.GET.get("email")
        password = request.GET.get("password")

        if email is None or password is None:
            return JsonResponse({"error": "Missing email or password!"}, status=400)

        register_response = maybe_register_user(email, password)
        return register_response


class Login(View):
    # Used to login users, and get the auth_token
    def get(self, request):
        email = request.GET.get("email")
        password = request.GET.get("password")

        if email is None or password is None:
            return JsonResponse({"error": "Missing email or password!"}, status=400)

        login_response = login_user(email, password)
        return login_response


class Bookings(View):
    # Used to get booking information.
    def get(self, request):
        auth_token = request.GET.get("auth_token")
        booking_id = request.GET.get("booking_id")

        if auth_token is None or booking_id is None:
            return JsonResponse(
                {"error": "Missing booking id or auth token"}, status=400
            )

        try:
            booking_id = int(booking_id)
        except ValueError:
            return JsonResponse({"error": "Booking Id must be an integer"}, status=400)

        booking_details = maybe_get_booking_details(auth_token, booking_id)
        return booking_details

    # Used to make a booking.
    def post(self, request):
        auth_token = request.GET.get("auth_token")
        train_id = request.GET.get("train_id")
        source = request.GET.get("source")
        destination = request.GET.get("destination")
        seats = request.GET.get("seats")

        required_parameters = [auth_token, train_id, source, destination, seats]

        if None in required_parameters:
            return JsonResponse({"error": "Incomplete details"}, status=400)

        try:
            train_id = int(train_id)
            source = int(source)
            destination = int(destination)
            seats = int(seats)
        except ValueError:
            return JsonResponse(
                {"error": "train id, source, destination and seats must be integers!"},
                status=400,
            )

        booking_info = maybe_process_booking(
            auth_token, train_id, source, destination, seats
        )

        return booking_info


class Seats(View):
    # Used to obtain available seats
    # between two stations in various
    # trains.
    def get(self, request):
        source = request.GET.get("source")
        destination = request.GET.get("destination")

        if source is None or destination is None:
            return JsonResponse(
                {"error": "source and destination can not be None"}, status=400
            )

        try:
            source = int(source)
            destination = int(destination)
        except ValueError:
            return JsonResponse(
                {"error": "source and destination must be of integer values"},
                status=400,
            )

        response = maybe_get_available_seats(source, destination)
        return response
