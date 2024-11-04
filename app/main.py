import streamlit as st
from PIL import Image
import os
from utils.moondream_integration import MoondreamModel
from utils.logger import logger

def initialize_model():
    try:
        model = MoondreamModel()
        return model
    except Exception as e:
        logger.error(f"Error initializing model: {str(e)}")
        raise

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = initialize_model()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("Moondream Vision Chat")

# Image upload
uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    try:
        # Display the image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # Save image temporarily
        temp_path = "temp_image.jpg"
        image.save(temp_path)
        
        # Process image and get caption
        with st.spinner('Analyzing image...'):
            caption = st.session_state.model.process_image(temp_path)
            st.write("**Initial Description:**", caption)
        
        # Chat interface
        user_question = st.text_input("Ask a question about the image:")
        if user_question:
            with st.spinner('Thinking...'):
                if len(user_question) > 50:  # Arbitrary threshold for longer questions
                    answer_placeholder = st.empty()
                    answer = ""
                    for token in st.session_state.model.ask_question(user_question, stream=True):
                        answer += token
                        answer_placeholder.write(answer)
                    final_answer = answer  # Store the complete answer
                else:
                    final_answer = st.session_state.model.ask_question(user_question)
                st.session_state.chat_history.append({"question": user_question, "answer": final_answer})
        
        # Display chat history
        if st.session_state.chat_history:
            st.write("**Chat History:**")
            for chat in st.session_state.chat_history:
                st.write(f"Q: {chat['question']}")
                st.write(f"A: {chat['answer']}")
        
        # Cleanup
        os.remove(temp_path)
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        logger.error(f"Error in main app: {str(e)}")