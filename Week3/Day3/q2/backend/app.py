from flask import Flask, request, jsonify
from recommendation_engine import recommend
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

@app.route("/api/recommend", methods=["POST"])
def get_recommendations():
    data = request.get_json()
    task_description = data.get("task", "")

    if not task_description.strip():
        return jsonify({"error": "Task description is required."}), 400

    try:
        results = recommend(task_description)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
