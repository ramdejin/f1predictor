from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .work import predict_winner

def predictor_view(request):
    """
    Serves the predictor HTML page.
    """
    return render(request, "predictions/predictor.html")

@csrf_exempt
def predict(request):
    """
    Handles the POST request for predicting the winner.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        race_name = data.get("race_name", "")
        weather = data.get("weather", 0)

        if not race_name:
            return JsonResponse({"error": "Race name is required"}, status=400)

        try:
            result = predict_winner(race_name, int(weather))
            return JsonResponse({"winner": result["winner"], "probabilities": result["probabilities"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)
