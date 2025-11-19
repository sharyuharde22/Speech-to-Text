print("RUNNING APP FROM:", __file__)  #To check from where the code is running i.e. folder 
from flask import Flask, render_template, request, jsonify
import whisper
import tempfile
import json
import datetime
import os

app = Flask(__name__)

# Load whisper model
model = whisper.load_model("tiny")   # tiny / base / small / medium / large

NOTES_FILE = "notes/notes.json"

# Load existing notes
def load_notes():
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except:
        return []

# Save notes
def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/speech_to_text", methods=["POST"])
def speech_to_text():
    audio_file = request.files["audio"]

    # save webm temporarily
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".webm").name
    audio_file.save(temp_path)

    # transcribe using whisper
    result = model.transcribe(temp_path)
    text = result["text"].strip()

    # delete temp file
    os.remove(temp_path)

    # save notes
    notes = load_notes()
    notes.append({
        "text": text,
        "time": str(datetime.datetime.now())
    })
    save_notes(notes)

    return jsonify({"text": text})

@app.route("/search", methods=["GET"])
def search_notes():
    query = request.args.get("q", "").lower()
    all_notes = load_notes()
    results = [n for n in all_notes if query in n["text"].lower()]
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
