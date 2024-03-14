from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from modules import db
from modules.event_categories import EventCategories
from modules.event_images import EventImages
from modules.events import Events
from modules.feedback import Feedback
from modules.registrations import Registrations
from modules.users import Users

bcrypt = Bcrypt()

def create_app():
    from routes import Routes
    app = Flask(__name__)
    app.config.from_pyfile('.config')
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    migrate = Migrate(app, db)
    bcrypt.init_app(app)
    
    routes_blueprint = Routes('routes', __name__)
    app.register_blueprint(routes_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        db.create_all()
    
        # are we gonna cry?
        
        
    app.run(debug=app.config['DEBUG'], use_reloader=app.config['USE_RELOADER'], port=5000)
    