from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import energy_consumption
import store_energy_data

app = Flask(__name__)

VALID_COOKIE = 'your_valid_cookie_value'

def authenticate(request):
    """Simple authentication based on a cookie."""
    auth_cookie = request.cookies.get('auth')
    return auth_cookie == VALID_COOKIE

@app.route('/api/energy-consumption', methods=['GET'])
def get_energy_consumption():
    """Endpoint to get aggregated energy consumption data."""
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    input_file_path = 'data/input.json'
    output_json = energy_consumption.main(input_file_path)
    return output_json, 200

@app.route('/api/store-energy-consumption', methods=['POST'])
def store_energy_consumption():
    """Endpoint to store energy consumption data and calculate aggregates."""
    if not authenticate(request):
        return jsonify({"error": "Unauthorized"}), 401

    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    
    store_energy_data.main(data)
    return jsonify({"message": "Data stored and aggregated successfully"}), 200

# Setup SwaggerUI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Energy Monitoring Service API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
