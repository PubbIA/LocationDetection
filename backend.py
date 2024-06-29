from flask import Flask, jsonify, request
from flask_cors import CORS
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app, resources={r"/bins": {"origins": "*"}})  # Autoriser toutes les origines pour /bins

# Données statiques des poubelles
bins = [
    {'id': 1, 'latitude': 34.0522, 'longitude': -118.2437 },
    {'id': 2, 'latitude': 36.1699, 'longitude': -115.1398},
    # Ajoute les autres poubelles ici
]


@app.route('/')
def hello():
    return 'Hello, World!'
# Route pour obtenir les poubelles à proximité
@app.route('/bins', methods=['GET', 'POST', 'OPTIONS'])
def manage_bins():
    if request.method == 'POST':
        data = request.json
        if 'latitude' not in data or 'longitude' not in data:
            return jsonify({'error': 'Latitude and longitude are required in JSON'}), 400

        user_lat = data['latitude']
        user_lng = data['longitude']

        nearby_bins = []
        user_location = (user_lat, user_lng)

        for bin in bins:
            bin_location = (bin['latitude'], bin['longitude'])
            distance = geodesic(user_location, bin_location).meters
            if distance <= 50:  # Distance en mètres
                bin['distance'] = distance
                nearby_bins.append(bin)

        return jsonify(nearby_bins)

    elif request.method == 'GET':
        return jsonify(bins)

if __name__ == '__main__':
    app.run(debug=True)
