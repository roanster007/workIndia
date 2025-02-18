from django.http import JsonResponse
from django.views import View
from railways.lib.admin import maybe_add_train_data

class Admin(View):
    # Used to add a train
    def post(self, request):
        API_KEY = request.GET.get("API_KEY")
        source = request.GET.get("source")
        destination = request.GET.get("destination")
        seats = request.GET.get("seats")

        required_parameters = [API_KEY, source, destination, seats]

        if None in required_parameters:
            return JsonResponse(
                {"error": "Incomplete Information"}, status=400
            )
        
        try:
            source = int(source)
            destination = int(destination)
            seats = int(seats)
        except ValueError:
            return JsonResponse(
                {"error": "Source and Destination, and seats must be integers"}, status=400
            )
        
        response = maybe_add_train_data(source, destination, seats, API_KEY)
        return response
        