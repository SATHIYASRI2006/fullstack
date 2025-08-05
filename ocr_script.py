import os
import re
import difflib
import pytesseract
from PIL import Image
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Configure Upload Folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tesseract Path Configuration
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if not os.path.exists(TESSERACT_PATH):
    raise FileNotFoundError(f"Tesseract not found at {TESSERACT_PATH}. Please check installation.")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Route: Upload Page
@app.route('/')
def upload_page():
    return render_template('upload.html')  # Ensure 'upload.html' is in the 'templates/' folder

# Route: Image Processing
@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    total_mark = request.form.get('total_mark')

    if not total_mark:
        return jsonify({"error": "Total mark not provided"}), 400

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        with Image.open(filepath) as img:
            extracted_text = pytesseract.image_to_string(img, config='--psm 6')

        # Regex Patterns to Find Total Mark
        patterns = [
            r'TOTAL\s+MARKS?\D{0,10}(\d{3,4})',
            r'TOTAL\s+MARS?\D{0,10}(\d{3,4})',
            r'TOTAL.*?(\d{3,4})',
            r'(\d{3,4})\s*/\s*\d{3,4}',
            r'\b(\d{3,4})\b\s*(PASS|FAIL)',
            r'\b0*(\d{3,4})\b\s*ZERO',
        ]

        extracted_mark = "Not found"
        matched_snippet = ""

        for pattern in patterns:
            match = re.search(pattern, extracted_text, re.IGNORECASE)
            if match:
                extracted_mark = match.group(1)
                matched_snippet = match.group(0)
                break

        # Fallback: fuzzy matching
        if extracted_mark == "Not found":
            words = extracted_text.split()
            for word in words:
                close = difflib.get_close_matches(total_mark, [word], n=1, cutoff=0.85)
                if close:
                    extracted_mark = close[0]
                    matched_snippet = word
                    break

        # ✅ Clean leading zeros for comparison
        cleaned_extracted = extracted_mark.lstrip("0") if extracted_mark != "Not found" else "Not found"
        is_match = cleaned_extracted == str(int(total_mark)) if cleaned_extracted != "Not found" else False

        return jsonify({
            "entered_total_mark": total_mark,
            "extracted_total_mark": cleaned_extracted,
            "match": is_match,
            "summary": [matched_snippet] if matched_snippet else []
        })

    except Exception as e:
        return jsonify({"error": f"OCR Failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
