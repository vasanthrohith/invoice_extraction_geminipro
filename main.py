import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-pro-vision")



def get_gemini_response(query,image,prompt):
    response = model.generate_content([query,image[0],prompt])
    return response.text

st.set_page_config("Invoice extraction")


st.header("Invoice extraction - gemini-pro-vision")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """


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


input = st.text_input("Enter your query",key="input")
uploaded_file=st.file_uploader("select a invoice img", type=["jpeg","jpg","png"])
image=""

if uploaded_file:
    image=Image.open(uploaded_file)
    st.image(uploaded_file,"upoaded image.",use_column_width=True)


submit_btn = st.button("Run")

if submit_btn:
    image_bytes = input_image_setup(uploaded_file)
    # print(image_bytes)
    response = get_gemini_response(query = input,image = image_bytes,prompt = input_prompt)
    st.subheader("Gemini AI response:")
    st.write(response)










