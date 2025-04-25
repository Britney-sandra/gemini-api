from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Create upload directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/ask', methods=['POST'])
def ask():
    # Check for file in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    # Check for question in form data
    if 'question' not in request.form:
        return jsonify({"error": "No question provided in the form"}), 400

    file = request.files['file']
    question = request.form.get('question')

    # If no file selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # You can add your Gemini API logic here to process the file + question

    # Respond back
    response = {
        "message": "File uploaded successfully!",
        "file_path": file_path,
        "question": question
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
