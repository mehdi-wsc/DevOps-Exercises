from flask import g, Flask, request, jsonify
from flask_cors import CORS
import os
from glob import glob
import importlib
from dotenv import load_dotenv
from errors import BaseApiError, ServerError


def register_app(application, routes_folder='routes'):
    @application.before_request
    def before_all():
        # Used to bypass CORS
        if request.method == "OPTIONS":
            return jsonify({}), 200

    @application.errorhandler(BaseApiError)
    def handle_invalid_usage(error):
        return error.to_json(), error.code

    @application.errorhandler(500)
    def internal_error(error):
        server_error = ServerError(str(error))
        return server_error.to_json(), server_error.code

    @application.errorhandler(404)
    def w404_error(e):
        server_error = BaseApiError(404, "Not found", "NotFound", e.description)
        return server_error.to_json(), server_error.code

    @application.teardown_appcontext
    def close_connection(_):
        db = getattr(g, '_database', None)
        if db is not None:
            db["db"].close()

    """
        Register all blueprints in folder
    """
    url_prefix = application.config['URL_PREFIX'] if 'URL_PREFIX' in application.config else ""

    for x in os.walk(routes_folder):
        for path in glob(os.path.join(x[0], '*.py')):
            folders, filename = os.path.split(path)
            strict_filename, extension = os.path.splitext(filename)
            current_dir = os.path.basename(folders)
            if filename != '__init__.py' and strict_filename.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
                potential_blueprint_name = current_dir+'_'+strict_filename
                folders_point = folders.replace('/', '.') + '.' + strict_filename
                route_path = folders[len(routes_folder):]
                #try:
                bp = importlib.import_module(folders_point, potential_blueprint_name)
                application.register_blueprint(getattr(bp, potential_blueprint_name), url_prefix=url_prefix+route_path)
                #except Exception as e:
                #    print("\033[91mRoute creation error : "+str(e)+"\033[0m")


def create_app():
    application = Flask(__name__)
    CORS(application, supports_credentials=True)
    register_app(application)
    return application


if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    app.run("0.0.0.0")
