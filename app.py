from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return 'Flask app is live!'

@app.route('/ask', methods=['POST'])
def ask():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    if 'question' not in request.form:
        return jsonify({"error": "No question provided in the form"}), 400

    file = request.files['file']
    question = request.form.get('question')

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({
        "message": "File uploaded successfully!",
        "file_path": file_path,
        "question": question
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
