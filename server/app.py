from flask import Flask, jsonify
from flask_cors import CORS

from routes.start_game import bp as start_game_bp
from routes.get_code import bp as get_code_bp
from routes.submit_turn import bp as submit_turn_bp
from routes.get_results import bp as get_report_bp

app = Flask(__name__)
CORS(app, origins="*")

@app.route("/api/test", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Flask backend!"})

app.register_blueprint(start_game_bp)
app.register_blueprint(get_code_bp)
app.register_blueprint(submit_turn_bp)
app.register_blueprint(get_report_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)




