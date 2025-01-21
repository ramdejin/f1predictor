import pandas as pd

# Load the 2023-2024 data
data_2023_2024 = pd.read_csv('final.csv')

# Define the 2022 data in a dictionary
data_2022 = {
    "year": [2022] * 22,
    "champion": ["Max Verstappen"] * 22,
    "constructor_champion": ["Red Bull Racing RBPT"] * 22,
    "races_in_season": [22] * 22,
    "drivers_in_season": [20] * 22,
    "teams_in_season": [10] * 22,
    "date": [
        "20 Mar 2022", "27 Mar 2022", "10 Apr 2022", "24 Apr 2022",
        "08 May 2022", "22 May 2022", "29 May 2022", "12 Jun 2022",
        "19 Jun 2022", "03 Jul 2022", "10 Jul 2022", "24 Jul 2022",
        "31 Jul 2022", "28 Aug 2022", "04 Sep 2022", "11 Sep 2022",
        "02 Oct 2022", "09 Oct 2022", "23 Oct 2022", "30 Oct 2022",
        "13 Nov 2022", "20 Nov 2022"
    ],
    "race_name": [
        "Bahrain Grand Prix", "Saudi Arabian Grand Prix", "Australian Grand Prix",
        "Emilia Romagna Grand Prix", "Miami Grand Prix", "Spanish Grand Prix",
        "Monaco Grand Prix", "Azerbaijan Grand Prix", "Canadian Grand Prix",
        "British Grand Prix", "Austrian Grand Prix", "French Grand Prix",
        "Hungarian Grand Prix", "Belgian Grand Prix", "Dutch Grand Prix",
        "Italian Grand Prix", "Singapore Grand Prix", "Japanese Grand Prix",
        "United States Grand Prix", "Mexican Grand Prix", "Brazilian Grand Prix",
        "Abu Dhabi Grand Prix"
    ],
    "circuit": [
        "Bahrain International Circuit", "Jeddah Corniche Circuit", "Albert Park Circuit",
        "Imola Circuit", "Miami International Autodrome", "Circuit de Barcelona–Catalunya",
        "Circuit de Monaco", "Baku City Circuit", "Circuit Gilles Villeneuve",
        "Silverstone Circuit", "Red Bull Ring", "Circuit Paul Ricard",
        "Hungaroring", "Circuit de Spa–Francorchamps", "Circuit Zandvoort",
        "Monza", "Marina Bay Street Circuit", "Suzuka Circuit",
        "Circuit of the Americas", "Autódromo Hermanos Rodríguez", "Interlagos",
        "Yas Marina Circuit"
    ],
    "weather": ["f"] * 22,
    "winner": [
        "Charles Leclerc", "Max Verstappen", "Charles Leclerc", "Max Verstappen",
        "Max Verstappen", "Max Verstappen", "Sergio Perez", "Max Verstappen",
        "Max Verstappen", "Carlos Sainz", "Charles Leclerc", "Max Verstappen",
        "Max Verstappen", "Max Verstappen", "Max Verstappen", "Max Verstappen",
        "Sergio Perez", "Max Verstappen", "Max Verstappen", "Max Verstappen",
        "George Russell", "Max Verstappen"
    ],
    "pole": ["Unknown"] * 22,
    "dotd": ["Unknown"] * 22,
    "fastest_lap": ["Unknown"] * 22,
}

# Convert 2022 data to DataFrame
df_2022 = pd.DataFrame(data_2022)

# Add missing columns to 2022 DataFrame
for column in data_2023_2024.columns:
    if column not in df_2022.columns:
        default_value = "Unknown" if data_2023_2024[column].dtype == "object" else 0
        df_2022[column] = default_value

# Ensure column order matches
df_2022 = df_2022[data_2023_2024.columns]

# Concatenate the data
combined_data = pd.concat([data_2023_2024, df_2022], ignore_index=True)

# Save to final combined CSV
combined_data.to_csv('combined_final.csv', index=False)





