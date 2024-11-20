import streamlit as st
from PIL import Image
import cohere

# Directly pass your Cohere API key here
cohere_api_key = "UvQcnNHSF42oPDGTWv6P9OpGrOCMb9lPgKOjxj3m"

# Initialize Cohere client
co = cohere.Client(cohere_api_key)

# Function to get response from Cohere
def get_cohere_response(input, image, prompt):
    # Assuming Cohere handles text prompts and images differently, you'll need to adjust
    # Cohere API can be used for text generation, but it doesn't natively handle images like Gemini does.
    # So for this example, we'll just send the text input to Cohere for generating a response.
    
    combined_input = f"Prompt: {prompt}\nInput: {input}\n"
    
    # Generate the response
    response = co.generate(
        model='command',  # Use the appropriate Cohere model
        prompt=combined_input,
        max_tokens=150
    )
    
    # Correct way to extract the generated text from the response
    return response.generations[0].text.strip()  # Extracts the text from the first generation

# Function to handle image file input
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Cohere Image Demo")

st.header("Cohere Application")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

# Define the input prompt for analysis
input_prompt = """
               You are an expert in nutrition. Analyze the food items in the image and calculate the total calories, 
               also provide the details of each food item with its calorie count in the following format:

               1. Item 1 - X calories
               2. Item 2 - Y calories
               ----
               ----
               """

# If the "Tell me about the image" button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_cohere_response(input, image_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)
