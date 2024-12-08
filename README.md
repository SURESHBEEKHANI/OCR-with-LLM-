Llama OCR
Llama OCR is a web-based application built with Streamlit that extracts structured text from images using Groq's Llama 3.2 Vision model. It allows users to upload images and retrieve extracted text in a clean, markdown format.

Features
Upload Images: Supports PNG, JPG, and JPEG formats.
OCR Text Extraction: Extracts and formats text into markdown.
Clear Results: Reset the app with the "Clear" button.
Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/llama-ocr.git
cd llama-ocr
2. Create and Activate a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file and add your Groq API key:

makefile
Copy code
GROQ_API_KEY=your_groq_api_key_here
5. Run the Application
bash
Copy code
streamlit run app.py
Usage
Upload an image from the sidebar.
Click "Extract Text 🔍" to process the image and extract text.
View the extracted text in markdown format.
Click "Clear 🗑️" to reset the app.
Build
Clone the repository to your local machine.
Install Python dependencies via pip install -r requirements.txt.
Run the app with streamlit run app.py to start building or testing locally.
License
This project is licensed under the MIT License.

Contact
For questions or issues, contact your_email@example.com.

Enjoy using Llama OCR! 🦙

