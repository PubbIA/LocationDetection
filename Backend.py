from flask import Flask, jsonify, request
from flask_cors import CORS
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app, resources={r"/bins": {"origins": "*"}})  # Autoriser toutes les origines pour /bins

# Données statiques des poubelles
bins = [
       {'id': 1, 'latitude': 33.983430, 'longitude': -6.809990},
    {'id': 2, 'latitude': 33.986430, 'longitude': -6.809990},
    # {'id': 3, 'latitude': 33.983970, 'longitude': -6.808700},
    {'id': 4, 'latitude': 33.983740, 'longitude': -6.808610}, 
]

# Route pour obtenir les poubelles à proximité
@app.route('/bins', methods=['GET', 'POST'])
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
            if distance <= 150:  # Distance en mètres
                bin['distance'] = distance
                nearby_bins.append(bin)
                #print all bins with distance
                print(nearby_bins)

        return jsonify(nearby_bins)
    

    elif request.method == 'GET':
        return jsonify(bins)

if __name__ == '__main__':
    app.run(debug=True)
