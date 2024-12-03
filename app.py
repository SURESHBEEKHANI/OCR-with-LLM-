import streamlit as st
from PIL import Image
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Groq API key
api_key = os.getenv("GROQ_API_KEY")

# Ensure the API key is provided
if not api_key:
    st.error("API key is not set. Please add your API key to the .env file.")
    st.stop()

# Configure the Streamlit app
st.set_page_config(
    page_title="Groq OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Groq API client
client = Groq(api_key=api_key)

# App title and description
st.title("🦙 Groq OCR")
st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Groq OCR!</p>', unsafe_allow_html=True)
st.markdown("---")

# Add a clear button
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("Clear 🗑️"):
        st.session_state.pop('ocr_result', None)
        st.rerun()

# Sidebar for image upload
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    # Read the uploaded file bytes
                    image_bytes = uploaded_file.getvalue()

                    # Perform OCR using Groq API
                    response = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[
                            {
                                "role": "user",
                                "content": (
                                    "Analyze the text in the provided image. Extract all readable content "
                                    "and present it in a structured Markdown format. Use headings, lists, "
                                    "or code blocks as appropriate for clarity and organization."
                                ),
                                "images": [image_bytes]
                            }
                        ],
                        temperature=1,
                        max_tokens=1024,
                        top_p=1,
                        stream=False
                    )

                    # Handle the API response
                    if response.success:
                        st.session_state['ocr_result'] = response.data["text"]
                    else:
                        st.error(f"API Error: {response.error_message}")

                except Exception as e:
                    st.error(f"Error processing the image: {str(e)}")

# Display OCR results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to view results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Groq OCR | [Report an Issue](https://github.com/patchy631/ai-engineering-hub/issues)")
