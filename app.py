import streamlit as st  # Streamlit for the web app interface
from groq import Groq  # Groq for handling the API requests
from PIL import Image  # PIL for image processing (opening, displaying images)
import os  # For file and environment variable handling
from dotenv import load_dotenv  # To load environment variables from .env file
import base64  # To encode images into base64 format
import io  # To handle in-memory byte buffers

# Load environment variables from .env file
load_dotenv()

# Retrieve the Groq API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")  # Retrieves the API key stored in the .env file

# Initialize the Groq client with the API key
client = Groq(api_key=api_key)  # Creates a Groq client object using the API key

# Page configuration for Streamlit
st.set_page_config(
    page_title="Llama OCR",  # Set the title of the app
    page_icon="🦙",  # Set the page icon (Llama emoji)
    layout="wide",  # Use a wide layout for the app
    initial_sidebar_state="expanded"  # Set the initial state of the sidebar to expanded
)

# Function to handle main content of the page
def main_content():
    st.title("🦙 Llama OCR")  # Display the main title
    st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Llama 3.2 Vision!</p>', unsafe_allow_html=True)  # Display a description below the title with custom styling
    st.markdown("---")  # Horizontal line to separate sections

    col1, col2 = st.columns([6, 1])  # Create two columns: a large left column and a smaller right column for the clear button
    with col2:
        if st.button("Clear 🗑️"):  # If the "Clear" button is clicked
            if 'ocr_result' in st.session_state:  # Check if OCR result exists in session state
                del st.session_state['ocr_result']  # Delete the OCR result from session state
            st.rerun()  # Rerun the app to reset everything

    # Display OCR result in the main content section (if it exists)
    if 'ocr_result' in st.session_state:
        st.markdown("### 🎯 **Extracted Text**")  # Professional heading with a target emoji to make it stand out
        st.markdown(st.session_state['ocr_result'], unsafe_allow_html=True)  # Display the OCR result stored in session state

# Function to handle sidebar content
def sidebar_content():
    with st.sidebar:  # Everything inside this block will appear in the sidebar
        st.header("📥 Upload Image")  # Sidebar header for the image upload section
        
        # Display message if no image is uploaded
        if 'ocr_result' not in st.session_state:
            st.write("### Please upload an image to extract text.")  # Instruction message to upload an image
        
        uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])  # Upload an image file with supported types

        if uploaded_file:  # If an image is uploaded
            display_uploaded_image(uploaded_file)  # Call function to display the uploaded image

        # This button triggers the processing of the uploaded image to extract text
        if uploaded_file and st.button("Extract Text 🔍") and 'ocr_result' not in st.session_state:
            with st.spinner("Processing image... Please wait."):  # Show a spinner during image processing
                process_image(uploaded_file)  # Call the function to process the image and extract text

        # If no image is uploaded or processed, clear the sidebar
        if not uploaded_file and 'ocr_result' not in st.session_state:
            st.sidebar.empty()  # Ensures the sidebar is empty unless there is interaction

# Function to display the uploaded image
def display_uploaded_image(uploaded_file):
    image = Image.open(uploaded_file)  # Open the uploaded image using PIL
    st.image(image, caption="Uploaded Image", use_container_width=True)  # Display the image in the app with a caption and automatic width

# Function to encode the image into base64 format
def encode_image(uploaded_file):
    image = Image.open(uploaded_file)  # Open the uploaded image
    buffered = io.BytesIO()  # Create an in-memory byte buffer
    image.save(buffered, format=image.format)  # Save the image into the buffer
    img_byte_array = buffered.getvalue()  # Get the byte array of the image
    return base64.b64encode(img_byte_array).decode('utf-8'), image.format  # Return the base64 encoded image and its format

# Function to process the image and extract text using Groq API
def process_image(uploaded_file):
    if uploaded_file:  # Check if an image is uploaded
        # Encode the uploaded image to base64 and retrieve the image format
        base64_image, image_format = encode_image(uploaded_file)

        # Determine the MIME type for the base64 encoded image
        mime_type = f"image/{image_format.lower()}"

        # Create a base64 URL for the image
        base64_url = f"data:{mime_type};base64,{base64_image}"

        # Start spinner while waiting for the API response
        with st.spinner("Generating response... This may take a moment."):
            try:
                # Call the Groq API to extract text from the image
                response = client.chat.completions.create(
                    model="llama-3.2-11b-vision-preview",  # Specify the model to use (Llama 3.2 Vision)
                    messages=[
                        {
                            "role": "user",  # Role of the message sender
                            "content": [  # The content of the message
                                {"type": "text", "text": "Analyze the text in the provided image. Extract all readable content "
                                    "and present it in a structured Markdown format. Use headings, lists, "
                                    "or code blocks as appropriate for clarity and organization."},
                                {
                                    "type": "image_url",  # Type of content: image
                                    "image_url": {
                                        "url": base64_url,  # The base64 URL of the uploaded image
                                    },
                                },
                            ]
                        }
                    ],
                    temperature=0.2,  # Set the temperature to 0.1 for less randomness and more focused results
                    max_tokens=200,  # Limit the maximum number of tokens (words) to 200 for shorter responses
                    top_p=0.5,  # Set top_p to 0.5 to control the diversity of generated text
                    stream=False  # Disable streaming of results
                )

                # Access the content of the response from the Groq API
                message_content = response.choices[0].message.content
                st.session_state['ocr_result'] = message_content  # Store the extracted text in session state

            except Exception as e:  # Catch any errors during the image processing
                st.error(f"Error during text extraction: {e}")  # Display the error message in the app

# Running the Streamlit app
if __name__ == "__main__":
    main_content()  # Display the main content (title, OCR result)
    sidebar_content()  # Display the sidebar content (image upload and processing)
