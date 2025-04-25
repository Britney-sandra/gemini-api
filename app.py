from flask import Flask, request, jsonify
import google.generativeai as genai
import pandas as pd
import os

app = Flask(__name__)

# Gemini setup
genai.configure(api_key="AIzaSyCysdzMHSO1-ETPfWyU4vTIhK34jsPlbQE")
model = genai.GenerativeModel('gemini-1.5-flash')

EXCEL_PATH = 'C:/Users/lenovo/Downloads/Brit Data.xlsx'

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Load Excel when question is asked, not at app startup
        df = pd.read_excel(EXCEL_PATH, sheet_name="Sheet1", engine="openpyxl")

        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"error": "Missing 'question'"}), 400

        # Grouping summary
        if "FinancialYear" in df.columns and "JobProfit" in df.columns:
            jobprofit_summary = df.groupby("FinancialYear")["JobProfit"].sum().to_string()
        else:
            jobprofit_summary = "JobProfit summary not available due to missing columns."

        dataset_description = f"""
This dataset comes from the 'Shipment' table.
Columns: {', '.join(df.columns)}
Summary (JobProfit by FinancialYear):
{jobprofit_summary}

Sample rows:
{df.head(10).to_string(index=False)}
"""

        prompt = f"""
You are a smart business analyst reviewing shipment data.
Dataset Info:
{dataset_description}

Question: {question}
Give a concise, clear answer using available data.
"""

        response = model.generate_content(prompt)
        return jsonify({"answer": response.text.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "✅ Gemini API is running!"

if __name__ == '__main__':
    print("Starting Gemini Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
