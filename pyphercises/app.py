from flask import Flask, jsonify
import version
app = Flask(__name__)

@app.route('/')
def return_version():
    app_dict = {
        "name": "BaseApp",
        "description": "First cut app",
        "version": version.__version__,
    }
    return jsonify(app_dict)

if __name__ == "__main__":
    app.run()