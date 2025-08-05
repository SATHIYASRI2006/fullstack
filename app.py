from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os
import re

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        entered_total = int(request.form['total_mark'])
        entered_sgpa = request.form['sgpa'].strip()
        entered_cgpa = request.form['cgpa'].strip()

        file_12th = request.files['marksheet_12th']
        file_cgpa = request.files['marksheet_cgpa']

        if file_12th.filename == '' or file_cgpa.filename == '':
            return render_template("index.html", result="❌ Both files must be selected!", color="red")

        # Save both files
        path_12th = os.path.join(UPLOAD_FOLDER, file_12th.filename)
        path_cgpa = os.path.join(UPLOAD_FOLDER, file_cgpa.filename)
        file_12th.save(path_12th)
        file_cgpa.save(path_cgpa)

        # ====== OCR for 12th Marksheet ======
        text_12th = pytesseract.image_to_string(Image.open(path_12th))
        print("12th OCR Text:\n", text_12th)

        # Extract total mark
        numbers = re.findall(r'\b\d{2,4}\b', text_12th)
        filtered_numbers = [int(n) for n in numbers if 100 <= int(n) <= 600]
        ocr_total = min(filtered_numbers, key=lambda x: abs(x - entered_total)) if filtered_numbers else 0
        total_match = (entered_total == ocr_total)

        # ====== OCR for CGPA/SGPA Marksheet ======
        text_cgpa = pytesseract.image_to_string(Image.open(path_cgpa))
        print("CGPA/SGPA OCR Text:\n", text_cgpa)

        sgpa_match = re.search(r"SGPA[:\s\-]*([0-9]\.\d{1,2})", text_cgpa, re.IGNORECASE)
        cgpa_match = re.search(r"CGPA[:\s\-]*([0-9]\.\d{1,2})", text_cgpa, re.IGNORECASE)

        extracted_sgpa = sgpa_match.group(1) if sgpa_match else "Not found"
        extracted_cgpa = cgpa_match.group(1) if cgpa_match else "Not found"

        is_sgpa_match = extracted_sgpa == entered_sgpa
        is_cgpa_match = extracted_cgpa == entered_cgpa

        # Final result summary
        if total_match and is_sgpa_match and is_cgpa_match:
            result = "✅ All values matched!"
            color = "green"
        else:
            result = "❌ Some values did not match."
            color = "red"

        return render_template("index.html",
                               result=result,
                               color=color,
                               entered_total=entered_total,
                               calculated_total=ocr_total,
                               extracted_numbers=filtered_numbers,
                               entered_sgpa=entered_sgpa,
                               extracted_sgpa=extracted_sgpa,
                               entered_cgpa=entered_cgpa,
                               extracted_cgpa=extracted_cgpa)

    except Exception as e:
        print(e)
        return render_template("index.html", result="❌ Error occurred: " + str(e), color="red")

if __name__ == '__main__':
    app.run(debug=True)
