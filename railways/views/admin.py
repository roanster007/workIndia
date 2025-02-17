from django.http import JsonResponse
from django.views import View
from railways.lib.admin import maybe_add_train_data

class Admin(View):
    # Used to add a train
    def post(self, request):
        api_key = request.GET.get("API_KEY")
        source = request.GET.get("source")
        destination = request.GET.get("destination")
        seats = request.GET.get("seats")

        if None in api_key, source, destination, seats:
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
        