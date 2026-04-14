from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from rag import HybridRAG

# 👇 Tell Flask where templates & static files are
app = Flask(
    __name__,
    template_folder=".",     # index.html is here
    static_folder="."        # css + js are here
)

UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

rag_instance = None


# ===================== ROUTES =====================

# Serve index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# Serve JS & CSS manually
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)


# Upload JSON
@app.route("/upload", methods=["POST"])
def upload_file():
    global rag_instance

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not file.filename.endswith(".json"):
        return jsonify({"error": "Only JSON files allowed"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 🔥 Rebuild RAG with new file
        rag_instance = HybridRAG(file_path=filepath)

        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ask questions
@app.route("/ask", methods=["POST"])
def ask():
    global rag_instance

    if rag_instance is None:
        return jsonify({"error": "Please upload a JSON file first"}), 400

    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Empty question"}), 400

    try:
        answer = rag_instance.ask(question)
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ===================== RUN =====================

if __name__ == "__main__":
    app.run(debug=True)