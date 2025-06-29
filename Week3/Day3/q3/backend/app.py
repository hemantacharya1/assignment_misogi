# app.py

from flask import Flask, request, jsonify
import importlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SUPPORTED_TOOLS = {
    "cursor": "optimizers.cursor",
    "copilot": "optimizers.copilot",
    "replit": "optimizers.replit",
    "codewhisperer": "optimizers.codewhisperer",
    "tabnine": "optimizers.tabnine"
    # Add more tools as modules are created
}


@app.route("/api/optimize", methods=["POST"])
def optimize_prompt():
    data = request.get_json()

    base_prompt = data.get("prompt")
    tool_key = data.get("tool")

    if not base_prompt or not tool_key:
        return jsonify({"error": "Missing 'prompt' or 'tool' in request."}), 400

    if tool_key not in SUPPORTED_TOOLS:
        return jsonify({"error": f"Tool '{tool_key}' not supported."}), 400

    try:
        module_path = SUPPORTED_TOOLS[tool_key]
        optimizer_module = importlib.import_module(module_path)

        result = optimizer_module.optimize_prompt(base_prompt)

        return jsonify({
            "optimized_prompt": result.get("optimized_prompt", ""),
            "explanation": result.get("explanation", "")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
