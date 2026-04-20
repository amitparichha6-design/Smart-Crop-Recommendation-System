# ============================================================
# Lookup tables: State-wise average soil and weather data
# Source: ICAR reports, IMD climate normals, soil survey data
# ============================================================

STATE_DATA = {
    "Andhra Pradesh":      {"N": 280, "P": 55,  "K": 210, "ph": 7.2, "temperature": 29.5, "humidity": 72, "rainfall": 967},
    "Arunachal Pradesh":   {"N": 260, "P": 48,  "K": 190, "ph": 5.8, "temperature": 18.0, "humidity": 82, "rainfall": 2782},
    "Assam":               {"N": 245, "P": 42,  "K": 170, "ph": 5.7, "temperature": 24.0, "humidity": 84, "rainfall": 1800},
    "Bihar":               {"N": 290, "P": 62,  "K": 230, "ph": 7.5, "temperature": 26.5, "humidity": 73, "rainfall": 1029},
    "Chhattisgarh":        {"N": 255, "P": 50,  "K": 200, "ph": 6.5, "temperature": 27.0, "humidity": 71, "rainfall": 1300},
    "Goa":                 {"N": 230, "P": 40,  "K": 160, "ph": 5.9, "temperature": 27.5, "humidity": 80, "rainfall": 2932},
    "Gujarat":             {"N": 265, "P": 58,  "K": 220, "ph": 7.8, "temperature": 30.0, "humidity": 60, "rainfall": 820},
    "Haryana":             {"N": 310, "P": 68,  "K": 250, "ph": 8.0, "temperature": 25.5, "humidity": 58, "rainfall": 617},
    "Himachal Pradesh":    {"N": 220, "P": 44,  "K": 175, "ph": 6.2, "temperature": 13.0, "humidity": 68, "rainfall": 1469},
    "Jharkhand":           {"N": 250, "P": 47,  "K": 185, "ph": 5.9, "temperature": 26.0, "humidity": 74, "rainfall": 1200},
    "Karnataka":           {"N": 270, "P": 52,  "K": 205, "ph": 6.8, "temperature": 27.0, "humidity": 70, "rainfall": 1139},
    "Kerala":              {"N": 235, "P": 41,  "K": 165, "ph": 5.5, "temperature": 27.5, "humidity": 85, "rainfall": 3055},
    "Madhya Pradesh":      {"N": 275, "P": 57,  "K": 215, "ph": 7.3, "temperature": 27.5, "humidity": 62, "rainfall": 1017},
    "Maharashtra":         {"N": 268, "P": 54,  "K": 208, "ph": 7.1, "temperature": 28.5, "humidity": 66, "rainfall": 1177},
    "Manipur":             {"N": 245, "P": 43,  "K": 172, "ph": 5.6, "temperature": 21.5, "humidity": 80, "rainfall": 1467},
    "Meghalaya":           {"N": 240, "P": 40,  "K": 168, "ph": 5.4, "temperature": 17.5, "humidity": 83, "rainfall": 2818},
    "Mizoram":             {"N": 238, "P": 39,  "K": 165, "ph": 5.5, "temperature": 20.5, "humidity": 81, "rainfall": 2400},
    "Nagaland":            {"N": 242, "P": 41,  "K": 170, "ph": 5.6, "temperature": 19.0, "humidity": 80, "rainfall": 1800},
    "Odisha":              {"N": 260, "P": 51,  "K": 198, "ph": 6.3, "temperature": 27.0, "humidity": 76, "rainfall": 1489},
    "Punjab":              {"N": 320, "P": 70,  "K": 258, "ph": 7.9, "temperature": 24.0, "humidity": 57, "rainfall": 649},
    "Rajasthan":           {"N": 245, "P": 46,  "K": 185, "ph": 8.2, "temperature": 31.0, "humidity": 42, "rainfall": 528},
    "Sikkim":              {"N": 225, "P": 43,  "K": 172, "ph": 5.8, "temperature": 14.5, "humidity": 78, "rainfall": 2739},
    "Tamil Nadu":          {"N": 275, "P": 55,  "K": 212, "ph": 7.0, "temperature": 28.5, "humidity": 74, "rainfall": 998},
    "Telangana":           {"N": 272, "P": 53,  "K": 207, "ph": 7.1, "temperature": 29.0, "humidity": 68, "rainfall": 960},
    "Tripura":             {"N": 243, "P": 42,  "K": 169, "ph": 5.7, "temperature": 24.5, "humidity": 82, "rainfall": 2000},
    "Uttar Pradesh":       {"N": 300, "P": 65,  "K": 240, "ph": 7.6, "temperature": 26.0, "humidity": 67, "rainfall": 896},
    "Uttarakhand":         {"N": 232, "P": 46,  "K": 178, "ph": 6.4, "temperature": 15.0, "humidity": 72, "rainfall": 1500},
    "West Bengal":         {"N": 278, "P": 58,  "K": 218, "ph": 6.2, "temperature": 26.5, "humidity": 79, "rainfall": 1582},
}

# Season mapping for yield model
SEASON_MAP = {
    "Kharif":      "Kharif     ",
    "Rabi":        "Rabi       ",
    "Whole Year":  "Whole Year ",
    "Summer":      "Summer     ",
    "Autumn":      "Autumn     ",
    "Winter":      "Winter     ",
}

# Crop emoji mapping for UI
CROP_EMOJI = {
    "rice": "🌾", "maize": "🌽", "chickpea": "🫘", "kidneybeans": "🫘",
    "pigeonpeas": "🫘", "mothbeans": "🫘", "mungbean": "🫘", "blackgram": "🫘",
    "lentil": "🫘", "pomegranate": "🍎", "banana": "🍌", "mango": "🥭",
    "grapes": "🍇", "watermelon": "🍉", "muskmelon": "🍈", "apple": "🍎",
    "orange": "🍊", "papaya": "🍈", "coconut": "🥥", "cotton": "🌿",
    "jute": "🌿", "coffee": "☕", "wheat": "🌾", "sugarcane": "🎋",
}

# Crop average market price in INR per quintal (for profit estimate)
CROP_PRICE_PER_QUINTAL = {
    "rice": 2183, "wheat": 2275, "maize": 1962, "chickpea": 5440,
    "lentil": 5500, "mungbean": 7755, "blackgram": 6600, "kidneybeans": 6000,
    "pigeonpeas": 6600, "mothbeans": 5450, "banana": 1500, "mango": 4000,
    "grapes": 5000, "watermelon": 800, "muskmelon": 1200, "apple": 8000,
    "orange": 3000, "papaya": 1500, "coconut": 2500, "cotton": 6380,
    "jute": 4500, "coffee": 18000, "sugarcane": 340, "pomegranate": 8000,
}

def get_state_data(state):
    """Return soil and weather data for a given state."""
    return STATE_DATA.get(state, STATE_DATA["Maharashtra"])  # default fallback

def get_all_states():
    return sorted(STATE_DATA.keys())
