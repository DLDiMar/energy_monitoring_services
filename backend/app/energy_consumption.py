from flask import Blueprint, request, jsonify

bp = Blueprint('energy_consumption', __name__)

@bp.route('/calculate', methods=['POST'])
def calculate_energy_consumption():
    data = request.json
    try:
        power = data['power']
        hours = data['hours']
        days = data['days']

        energy_consumption = (power * hours * days) / 1000

        return jsonify({'energy_consumption_kwh': energy_consumption}), 200

    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
