import streamlit as st
from utils.message_formatter import format_message_for_display

def render_game_description_input():
    return st.text_area(
        "Describe your game:",
        placeholder="Example: A simple snake game where the snake grows when eating food. Include arrow key controls and score display.",
        help="Describe the game you want - be specific about features!"
    )

def render_control_buttons(conversation, initial_question):
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        if not st.session_state.started:
            if st.button("Start Creating Game", type="primary"):
                if initial_question:
                    st.session_state.conversation = conversation
                    st.session_state.conversation.start_conversation(initial_question)
                    st.session_state.started = True
                else:
                    st.error("Please describe the game you want to create")
        else:
            if st.button("Stop Development", type="secondary"):
                st.session_state.conversation.stop_conversation()
                st.session_state.started = False

def render_game_versions(conversation):
    st.markdown("### 📦 Game Versions")
    if conversation.code_versions:
        for version in reversed(conversation.code_versions):
            with st.expander(f"Version {version.version_number}", expanded=True):
                st.markdown(f"**What's New:**\n{version.description}")
                st.markdown("**How to Run:**")
                st.code(version.run_instructions)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    filename = f"game_v{version.version_number}.py"
                    st.download_button(
                        label=f"💾 Download Game",
                        data=version.code,
                        file_name=filename,
                        mime="text/plain"
                    )
                with col_b:
                    if st.button(f"👀 View Code", key=f"view_code_{version.version_number}"):
                        st.code(version.code, language="python")

def render_development_progress(conversation):
    st.markdown("### 💬 Development Progress")
    
    for entry in conversation.conversation_history:
        if entry["speaker"] == "AI 1":
            color = "#e6f3ff"
            icon = "🤖"
        elif entry["speaker"] == "AI 2":
            color = "#fff2e6"
            icon = "🤖"
        elif entry["speaker"] == "System":
            color = "#e6ffe6"
            icon = "✨"
        else:
            color = "#ffe6e6"
            icon = "⚠️"

        message_html = f"""
            <div style='background-color: {color}; border-radius: 10px; padding: 10px; margin: 5px 0;'>
                <strong>{icon} {entry["speaker"]} ({entry["timestamp"]}):</strong>
            </div>
        """
        st.markdown(message_html, unsafe_allow_html=True)
        st.markdown(format_message_for_display(entry["message"]))