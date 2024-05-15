from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuration settings can be added here
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///energy_data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Register Blueprints or routes here
    with app.app_context():
        from . import energy_consumption, store_energy_data
        app.register_blueprint(energy_consumption.bp)
        app.register_blueprint(store_energy_data.bp)

    return app
