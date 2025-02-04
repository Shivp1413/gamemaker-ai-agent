import streamlit as st
import time
from models.llm_conversation import LLMConversation
from ui.streamlit_app import (
    render_game_description_input,
    render_control_buttons,
    render_game_versions,
    render_development_progress
)

def main():
    st.set_page_config(page_title="GameMaker AI Agent", layout="wide")
    st.title("🎮 GameMaker AI Agent")
    
    if 'conversation' not in st.session_state:
        st.session_state.conversation = LLMConversation()
    
    if 'started' not in st.session_state:
        st.session_state.started = False

    col1, col2 = st.columns([2, 1])
    
    with col1:
        initial_question = render_game_description_input()
        render_control_buttons(st.session_state.conversation, initial_question)

    with col2:
        render_game_versions(st.session_state.conversation)

    # Process queue
    while not st.session_state.conversation.queue.empty():
        speaker, message = st.session_state.conversation.queue.get_nowait()
        st.session_state.conversation.add_to_history(speaker, message)
        st.rerun()

    render_development_progress(st.session_state.conversation)

    if st.session_state.started:
        time.sleep(0.1)
        st.rerun()

if __name__ == "__main__":
    main()