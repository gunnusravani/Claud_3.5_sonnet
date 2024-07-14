import os
from dotenv import load_dotenv
import anthropic
import base64
import httpx
import streamlit as st
from PIL import Image
from io import BytesIO
# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=api_key)

def analyze_handwriting(image):

    buffered = BytesIO()
    image.save(buffered,format=image.format)
    image_data = base64.b64encode(buffered.getvalue()).decode()
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source":{
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }

                    },
                    {
                        "type": "text",
                        "text": """ 
                        please analyze this handwriting or signature.
                        Describe the characteristics you observe and what they might indicate about the writer.
                        Include aspects like pressure, slant, size, spacing, and any other notable features.
                        """
                    }
                ]
            }
        ]
    )
    return response.content[0].text

st.title("✍ Handwriting Analyzer")

uploaded_file = st.file_uploader("choose an image of handwriting or a signature", type=["png","jpg","jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Handwriting"):
        with st.spinner("Analyzing..."):
            analysis = analyze_handwriting(image)
            st.subheader("Analysis Results:")
            st.write(analysis)