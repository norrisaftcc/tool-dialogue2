"""
Streamlit Interface for Dialogue Tree System.
A simple UI for interactive dialogue trees.
"""
import streamlit as st
import json
import os
from dialogue_lib import DialogueManager


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "manager" not in st.session_state:
        st.session_state.manager = DialogueManager()
    
    if "dialogue_loaded" not in st.session_state:
        st.session_state.dialogue_loaded = False
    
    if "current_dialogue" not in st.session_state:
        st.session_state.current_dialogue = None
    
    if "dialogue_history" not in st.session_state:
        st.session_state.dialogue_history = []


def load_dialogue_file(file_path):
    """Load dialogue from file path"""
    success = st.session_state.manager.load_dialogue_file(file_path)
    
    if success:
        st.session_state.dialogue_loaded = True
        st.session_state.current_dialogue = st.session_state.manager.get_current_dialogue()
        st.session_state.dialogue_history = []
        
        # Add first dialogue to history
        if st.session_state.current_dialogue:
            st.session_state.dialogue_history.append({
                "npc_name": st.session_state.current_dialogue["npc_name"],
                "text": st.session_state.current_dialogue["text"]
            })
    
    return success


def handle_response(response_id):
    """Handle user response selection"""
    success = st.session_state.manager.choose_response(response_id)
    
    if success:
        new_dialogue = st.session_state.manager.get_current_dialogue()
        st.session_state.current_dialogue = new_dialogue
        
        if new_dialogue:
            # Add to dialogue history
            st.session_state.dialogue_history.append({
                "npc_name": new_dialogue["npc_name"],
                "text": new_dialogue["text"]
            })


def reset_dialogue():
    """Reset to the starting dialogue"""
    st.session_state.manager.reset_dialogue()
    st.session_state.current_dialogue = st.session_state.manager.get_current_dialogue()
    st.session_state.dialogue_history = []
    
    # Add first dialogue to history
    if st.session_state.current_dialogue:
        st.session_state.dialogue_history.append({
            "npc_name": st.session_state.current_dialogue["npc_name"],
            "text": st.session_state.current_dialogue["text"]
        })


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Dialogue System",
        page_icon="💬",
        layout="centered"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Custom CSS for basic styling
    st.markdown("""
    <style>
        .dialogue-box {
            background-color: #f0f0f0;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        .npc-name {
            font-weight: bold;
            color: #4b5c78;
        }
        
        .history-box {
            opacity: 0.8;
            padding-bottom: 5px;
            margin-bottom: 10px;
            border-bottom: 1px solid #ddd;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Application header
    st.title("Dialogue System")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        
        # File loading options
        st.subheader("Load Dialogue File")
        
        # Default files
        dialogue_dir = "../json"
        if os.path.exists(dialogue_dir):
            json_files = [f for f in os.listdir(dialogue_dir) if f.endswith('.json')]
            if json_files:
                selected_file = st.selectbox(
                    "Select from available files:",
                    [""] + [os.path.join(dialogue_dir, f) for f in json_files]
                )
                
                if selected_file:
                    if st.button("Load Selected File"):
                        with st.spinner("Loading dialogue..."):
                            if load_dialogue_file(selected_file):
                                st.success("Dialogue loaded successfully!")
                            else:
                                st.error("Failed to load dialogue. Check file format.")
        
        # Reset button
        if st.session_state.dialogue_loaded:
            if st.button("Reset Dialogue"):
                reset_dialogue()
    
    # Main content area
    if not st.session_state.dialogue_loaded:
        st.markdown(
            '<div class="dialogue-box">'
            '<p>Welcome to the Dialogue System.</p>'
            '<p>Please load a dialogue file using the sidebar options.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        # Display dialogue interface
        
        # Display dialogue history
        for i, entry in enumerate(st.session_state.dialogue_history[:-1]):
            st.markdown(
                f'<div class="history-box">'
                f'<span class="npc-name">[{entry["npc_name"]}]</span><br>'
                f'{entry["text"]}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Display current dialogue
        if st.session_state.current_dialogue:
            current = st.session_state.dialogue_history[-1]
            st.markdown(
                f'<div class="dialogue-box">'
                f'<span class="npc-name">[{current["npc_name"]}]</span><br>'
                f'{current["text"]}'
                f'</div>',
                unsafe_allow_html=True
            )
            
            # Display response options
            st.write("Your Response:")
            
            for response in st.session_state.current_dialogue["responses"]:
                if st.button(response["text"], key=response["id"]):
                    handle_response(response["id"])
                    st.experimental_rerun()


if __name__ == "__main__":
    main()