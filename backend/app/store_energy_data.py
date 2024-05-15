from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime

bp = Blueprint('store_energy_data', __name__)

def init_db():
    conn = sqlite3.connect('energy_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS energy_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    power REAL,
                    hours REAL,
                    days INTEGER,
                    energy_consumption_kwh REAL,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

@bp.route('/store', methods=['POST'])
def store_energy_data():
    data = request.json
    try:
        power = data['power']
        hours = data['hours']
        days = data['days']

        energy_consumption = (power * hours * days) / 1000

        conn = sqlite3.connect('energy_data.db')
        c = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO energy_data (power, hours, days, energy_consumption_kwh, timestamp) VALUES (?, ?, ?, ?, ?)',
                  (power, hours, days, energy_consumption, timestamp))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Energy data stored successfully', 'energy_consumption_kwh': energy_consumption}), 200

    except KeyError as e:
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
