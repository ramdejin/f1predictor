from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from .work import predict_winner
from difflib import get_close_matches


def home(request):
    return render(request, 'predictions/home.html')

def predictor(request):
    """
    Serves the predictor HTML page.
    """
    return render(request, "predictions/predictor.html")

def visualizer(request):
    return render(request, 'predictions/visualizer.html')

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

def filter_view(request):
    return render(request, 'predictions/filter.html')


def filter_search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({"error": "No query provided"})

    try:
        # Load the points.csv data
        points_df = pd.read_csv('points.csv')

        # Standardize the Driver column (remove spaces, ensure lowercase)
        points_df['Driver'] = points_df['Driver'].str.strip().str.lower()

        # Convert the query to lowercase for case-insensitive matching
        query_lower = query.lower()

        # Filter rows if query matches first letters
        filtered_rows = points_df[points_df['Driver'].str.startswith(query_lower)]

        # If no rows match the exact query, find the most similar driver using difflib
        if filtered_rows.empty:
            closest_match = get_close_matches(query_lower, points_df['Driver'], n=1)
            if closest_match:
                driver_name = closest_match[0]
                filtered_rows = points_df[points_df['Driver'] == driver_name]

        # If still no match, return an error
        if filtered_rows.empty:
            return JsonResponse({"error": "No matching driver found"})

        # Convert filtered rows to a list of dictionaries for output
        result = filtered_rows.to_dict(orient='records')

        # Format the output as a readable JSON response
        readable_results = [
            {key: str(value) for key, value in row.items()} for row in result
        ]

        return JsonResponse({"data": readable_results})
    except Exception as e:
        return JsonResponse({"error": str(e)})

