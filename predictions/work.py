import numpy as np

# Preloaded model parameters
coefficients = [
    [-0.350688701388172, 1.7904166871887428],
    [-0.3919913677858248, 2.067006187518508],
    [-1.3898126702534064, -2.570661688773762],
    [-0.283601688954562, 1.3428105868705627],
    [-1.3898126702534062, -2.570661688773762],
    [4.089508787589934, -1.4017206709008672],
    [-0.283601688954562, 1.3428105868705627]
]
intercepts = [-0.7137032463732002, -0.5624405619135262, 1.6939486225988531,
              -1.010243971728873, 1.693948622598853, -0.09126549345325434, -1.010243971728873]
winner_classes = {
    "0": "Carlos Sainz Jr.",
    "1": "Charles Leclerc",
    "2": "George Russell",
    "3": "Lando Norris",
    "4": "Lewis Hamilton",
    "5": "Max Verstappen",
    "6": "Oscar Piastri"
}

race_mapping = {
    "Bahrain Grand Prix": 0,
    "Saudi Arabian Grand Prix": 1,
    "Australian Grand Prix": 2,
    "Chinese Grand Prix": 3,
    "Miami Grand Prix": 4,
    "Emilia Romagna Grand Prix": 5,
    "Monaco Grand Prix": 6,
    "Canadian Grand Prix": 7,
    "Spanish Grand Prix": 8,
    "Austrian Grand Prix": 9,
    "British Grand Prix": 10,
    "Hungarian Grand Prix": 11,
    "Belgian Grand Prix": 12,
    "Dutch Grand Prix": 13,
    "Italian Grand Prix": 14,
    "Singapore Grand Prix": 15,
    "Japanese Grand Prix": 16,
    "United States Grand Prix": 17,
    "Mexican Grand Prix": 18,
    "São Paulo Grand Prix": 19,
    "Las Vegas Grand Prix": 20,
    "Qatar Grand Prix": 21
}

def predict_winner(race_name, weather):
    """
    Predicts the race winner based on race name and weather input.

    Args:
        race_name (str): The name of the race.
        weather (int): Weather condition (0 for dry, 1 for rainy).

    Returns:
        dict: Predicted winner and probabilities.
    """
    # Prepare features vector with only two features: race_name and weather
    features = np.zeros(2)

    # Encode weather
    features[1] = weather

    # Encode race_name
    if race_name in race_mapping:
        features[0] = race_mapping[race_name]
    else:
        print("Race name not found in mapping. Defaulting to 0.")
        features[0] = 0

    # Calculate logits
    logits = np.array(intercepts) + np.dot(np.array(coefficients), features)

    # Apply softmax
    probabilities = np.exp(logits) / np.sum(np.exp(logits))
    predicted_index = np.argmax(probabilities)
    predicted_winner = winner_classes[str(predicted_index)]

    return {
        "winner": predicted_winner,
        "probabilities": probabilities.tolist()
    }
