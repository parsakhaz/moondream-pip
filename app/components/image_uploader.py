import streamlit as st
from PIL import Image
from utils.moondream_integration import MoondreamModel
from utils.logger import logger

class ImageUploader:
    @staticmethod
    def upload_and_describe():
        try:
            st.header("Upload an Image")
            uploaded_file = st.file_uploader(
                "Choose an image...", 
                type=["jpg", "jpeg", "png"],
                help="Upload an image to analyze"
            )
            
            if uploaded_file is not None:
                logger.info(f"New image uploaded: {uploaded_file.name}")
                image = Image.open(uploaded_file).convert('RGB')
                st.image(image, caption='Uploaded Image.', use_column_width=True)
                
                with st.spinner('Analyzing image...'):
                    model = MoondreamModel()
                    description, image_key = model.describe_image(image)
                    logger.info(f"Generated description for image {image_key[:8]}")
                
                return image_key, description
                
        except Exception as e:
            logger.error(f"Error in image upload: {str(e)}")
            st.error("An error occurred while processing the image. Please try again.")
            
        return None, None 