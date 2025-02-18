from django.http import JsonResponse
from django.views import View
from railways.lib.users import maybe_register_user, maybe_get_booking_details, login_user

class Register(View):
    # Used to register a user
    def post(self, request):
        email = request.GET.get("email")
        password = request.GET.get("password")

        if email is None or password is None:
            return JsonResponse(
                {"error": "Missing email or password!"}, status=400
            )
        
        register_response = maybe_register_user(email, password)
        return register_response


class Login(View):
    def post(self, request):
        email = request.GET.get("email")
        password = request.GET.get("password")

        if email is None or password is None:
            return JsonResponse(
                {"error": "Missing email or password!"}, status=400
            )
        
        login_response = login_user(email, password)
        return login_response
    

class Bookings(View):
    # Used to get booking information.
    def get(self, request):
        auth_token = request.GET.get("auth_token")
        booking_id = request.GET.get("bookind_id")

        if auth_token is None or bookind_id is None:
            return JsonResponse(
                {"error": "Missing booking id or auth token"}, status=400
            )
        
        try:
            bookind_id = int(bookind_id)
        except ValueError:
            retrun JsonResponse(
                {"error": "Booking Id must be an integer"}, status=400
            )
        
        booking_details = maybe_get_booking_details(auth_token, bookind_id)
        return booking_details
