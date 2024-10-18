import streamlit as st 
import os 
from dotenv import load_dotenv
import base64
from openai import OpenAI


load_dotenv()
key = os.getenv('OPENAI_API_KEY')
MODEL = 'gpt-4o'
client = OpenAI(api_key=key)

def encode_image(image):
    return base64.b64encode(image.read()).decode('utf-8')

st.title('图像分析仪')
image_file = st.file_uploader('上传图像文件', type=['png', 'jpg', 'jpeg'])
if image_file:
    st.image(image_file, caption='上传的图像', use_column_width=True)

    base64_image = encode_image(image_file)

    # Update the prompt to instruct the AI to respond in Chinese
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds in Markdown."},
            {"role": "user", "content": [
                {"type": "text", "text": "你能描述这张图片并生成一份报告，突出重要细节并提供建议。用项目符号创建包含观察、重要细节和建议的报告。"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )

    # Display the response in markdown format
    st.markdown(response.choices[0].message.content)
