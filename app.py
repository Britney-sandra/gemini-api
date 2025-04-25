import os
from flask import Flask, request, jsonify
import pandas as pd
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Set the folder for file uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set your Gemini API Key here
GENIE_API_KEY = 'AIzaSyCysdzMHSO1-ETPfWyU4vTIhK34jsPlbQE'
genai.configure(api_key=GENIE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/ask', methods=['POST'])
def ask_question():
    # Check if the file and question are present in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    if 'question' not in request.form:
        return jsonify({"error": "No question provided"}), 400

    # Get the file and question
    file = request.files['file']
    question = request.form['question']

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Read the Excel file using pandas
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to read Excel file: {str(e)}"}), 500

    # Create the prompt for the Gemini API
    prompt = f"""You are an analyst. Here is an Excel dataset:
{df.to_string(index=False)}

Question: {question}
"""

    # Send the prompt to the Gemini API and get the response
    try:
        response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        return jsonify({"error": f"Failed to communicate with Gemini API: {str(e)}"}), 500

    # Return the answer from the Gemini API
    return jsonify({"answer": answer}), 200


if __name__ == '__main__':
    # Port configuration for the production environment (like Render or Heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
