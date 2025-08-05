📄 Verify 12th Mark, SGPA, and CGPA (OCR Based) 
This is a simple PHP web app that verifies the entered 12th grade marks, SGPA, and CGPA by extracting values from uploaded scanned mark sheets using OCR (Optical Character Recognition).

✅ Features:

- 🖼️ Marksheet image upload (JPEG/PNG)
- 🔍 Extract text using Tesseract OCR
- ✅ Verify total marks between entered and extracted value
- 🗃️ Store verified data to admin database
- ❌ Reject mismatched data and log the attempt


🖼️ Demo

Initial screen
<img width="100" alt="Screenshot 2025-08-05 084939" src="https://github.com/user-attachments/assets/51b4e639-56a8-4e3c-b103-6013bb61853f" />



All values matched ✅
<img width="100" alt="Screenshot 2025-08-05 085035" src="https://github.com/user-attachments/assets/39835031-7dcb-45b7-becc-d764d463472a" />

Mismatch in values ❌
<img width="100" alt="Screenshot 2025-08-05 085000" src="https://github.com/user-attachments/assets/53af85e8-35d4-4d1c-8015-0186a288bb2b" />



⚙️ How It Works

User enters:
Total Mark (12th)
SGPA
CGPA

Uploads:

12th Marksheet
SGPA/CGPA Marksheet

PHP handles:
File upload
OCR using Tesseract or similar
Extracts numbers from the image
Compares them with user input
Displays result

🚀 Getting Started
Prerequisites

- Python 🐍
- Flask 🌐
- Tesseract OCR 🔎
- HTML, CSS 🎨
- SQLite or MySQL (as database)

Install Tesseract (Windows)
Download: https://github.com/tesseract-ocr/tesseract
Make sure to add it to your system PATH.



📁 Folder Structure

ocr_project/
├── app.py # Main Flask app
├── import pytesseract.py # OCR logic
├── ocr_script.py # Supporting OCR script
├── CREATE DATABASE marksheet_db;.sql # SQL to create database
├── index (2).html # Old/alternate HTML file
├── mismatches.txt # Log of mismatched entries
├── sample_image.png # Sample image
├── static/
│ ├── style.css # CSS styling
│ └── uploads/ # Uploaded images
├── templates/
│ └── index.html # Main HTML template

