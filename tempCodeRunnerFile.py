from flask import Flask, jsonify, request
from geopy.distance import geodesic

app = Flask(__name__)

# Données statiques des poubelles
bins = [
    {'id': 1, 'latitude': 34.0522, 'longitude': -118.2437 },
    {'id': 2, 'latitude': 36.1699, 'longitude': -115.1398},
    # Ajoute les autres poubelles ici
]

# Route pour obtenir les poubelles à proximité
@app.route('/bins', methods=['GET'])
def get_nearby_bins():
    # Récupère la latitude et la longitude de la requête
    user_lat = request.args.get('latitude', type=float)
    user_lng = request.args.get('longitude', type=float)
    
    if user_lat is None or user_lng is None:
        return jsonify({'error': 'Latitude and longitude are required'}), 400
    
    nearby_bins = []
    user_location = (user_lat, user_lng)
    
    for bin in bins:
        bin_location = (bin['latitude'], bin['longitude'])
        distance = geodesic(user_location, bin_location).meters
        if distance <= 50:  # Distance en mètres
            bin['distance'] = distance
            nearby_bins.append(bin)
    
    return jsonify(nearby_bins)

if __name__ == '__main__':
    app.run(debug=True)


#   leafletmap ----> hide-borders

# 1- my position centre  --->(cercle 100m) rayon 100 m 
# 2- poubelles --->(langitude, latitude inclus dans le cercle de 100m )
# 3- complexity down to O(n)  (n = number of bins)


