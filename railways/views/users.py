from django.http import JsonResponse
from django.views import View
from railways.lib.users import maybe_register_user, login_user

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
    
        

    

        
