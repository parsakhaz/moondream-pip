import streamlit as st
from utils.moondream_integration import MoondreamModel
from utils.logger import logger

class ChatInterface:
    @staticmethod
    def chat(image_key):
        try:
            st.header("Ask a Question About the Image")
            user_question = st.text_input(
                "Your Question:",
                help="Ask anything about the image"
            )
            
            if st.button("Submit", type="primary"):
                if user_question:
                    logger.info(f"New question for image {image_key[:8]}: {user_question}")
                    with st.spinner('Generating answer...'):
                        model = MoondreamModel()
                        answer = model.answer_question(image_key, user_question)
                        
                        # Store in session state
                        st.session_state.chat_history.append({
                            "question": user_question,
                            "answer": answer
                        })
                    
                    # Display chat history
                    st.subheader("Chat History")
                    for chat in st.session_state.chat_history:
                        st.text_area("Question", chat["question"], disabled=True)
                        st.text_area("Answer", chat["answer"], disabled=True)
                        st.divider()
                        
                else:
                    st.warning("Please enter a question.")
                    
        except Exception as e:
            logger.error(f"Error in chat interface: {str(e)}")
            st.error("An error occurred while processing your question. Please try again.") 