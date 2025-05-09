"""
Dialogue Editor for the Dialogue Tree System.
A Streamlit-based editor for creating and modifying dialogue trees.
"""
import streamlit as st
import json
import os
import uuid
from dialogue_lib import DialogueManager

# Define constants
DEFAULT_NEW_DIALOGUE = {
    "starting_dialogue": "",
    "dialogues": []
}

def generate_id(prefix="dlg"):
    """Generate a unique ID for new dialogue nodes"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "manager" not in st.session_state:
        st.session_state.manager = DialogueManager()
    
    if "dialogue_loaded" not in st.session_state:
        st.session_state.dialogue_loaded = False
    
    if "current_dialogue" not in st.session_state:
        st.session_state.current_dialogue = None
        
    if "dialogue_data" not in st.session_state:
        st.session_state.dialogue_data = DEFAULT_NEW_DIALOGUE.copy()
        
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = "tree"  # Options: "tree", "node", "response"
        
    if "selected_node_id" not in st.session_state:
        st.session_state.selected_node_id = None
        
    if "selected_response_id" not in st.session_state:
        st.session_state.selected_response_id = None
        
    if "modified" not in st.session_state:
        st.session_state.modified = False


def load_dialogue_file(file_path):
    """Load dialogue from file path"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            st.session_state.dialogue_data = json.load(f)
            
        # Also load into the manager for validation
        success = st.session_state.manager.load_dialogue_file(file_path)
        
        if success:
            st.session_state.dialogue_loaded = True
            st.session_state.modified = False
            return True
        return False
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return False


def save_dialogue_file(file_path):
    """Save dialogue to file path"""
    try:
        # Ensure the dialogues are in the correct format
        if not st.session_state.dialogue_data.get("starting_dialogue") and st.session_state.dialogue_data.get("dialogues"):
            # Set first dialogue as starting dialogue if not set
            st.session_state.dialogue_data["starting_dialogue"] = st.session_state.dialogue_data["dialogues"][0]["id"]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.dialogue_data, f, indent=2)
            
        st.session_state.modified = False
        return True
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return False


def create_new_dialogue():
    """Create a new blank dialogue tree"""
    st.session_state.dialogue_data = DEFAULT_NEW_DIALOGUE.copy()
    st.session_state.dialogue_loaded = True
    st.session_state.modified = True
    st.session_state.selected_node_id = None
    
    # Add the first dialogue node
    first_node_id = generate_id()
    st.session_state.dialogue_data["dialogues"].append({
        "id": first_node_id,
        "npc_name": "Character",
        "text": "Enter dialogue text here.",
        "responses": []
    })
    st.session_state.dialogue_data["starting_dialogue"] = first_node_id
    st.session_state.selected_node_id = first_node_id


def add_new_dialogue_node():
    """Add a new dialogue node to the tree"""
    new_id = generate_id()
    
    new_node = {
        "id": new_id,
        "npc_name": "Character",
        "text": "Enter dialogue text here.",
        "responses": []
    }
    
    st.session_state.dialogue_data["dialogues"].append(new_node)
    st.session_state.modified = True
    return new_id


def add_response_to_node(node_id):
    """Add a new response to a dialogue node"""
    for node in st.session_state.dialogue_data["dialogues"]:
        if node["id"] == node_id:
            new_response_id = generate_id("resp")
            
            # Create a new dialogue node for this response to connect to
            new_node_id = add_new_dialogue_node()
            
            node["responses"].append({
                "id": new_response_id,
                "text": "Enter response text",
                "next_dialogue": new_node_id
            })
            
            st.session_state.modified = True
            break


def delete_node(node_id):
    """Delete a dialogue node and all references to it"""
    # First, check if this is the starting dialogue
    if st.session_state.dialogue_data["starting_dialogue"] == node_id:
        st.error("Cannot delete the starting dialogue node. Set another node as starting first.")
        return False
    
    # Remove the node
    st.session_state.dialogue_data["dialogues"] = [
        node for node in st.session_state.dialogue_data["dialogues"] 
        if node["id"] != node_id
    ]
    
    # Remove any responses pointing to this node
    for node in st.session_state.dialogue_data["dialogues"]:
        node["responses"] = [
            resp for resp in node["responses"]
            if resp["next_dialogue"] != node_id
        ]
    
    st.session_state.modified = True
    st.session_state.selected_node_id = None
    return True


def delete_response(node_id, response_id):
    """Delete a response from a dialogue node"""
    for node in st.session_state.dialogue_data["dialogues"]:
        if node["id"] == node_id:
            node["responses"] = [
                resp for resp in node["responses"]
                if resp["id"] != response_id
            ]
            st.session_state.modified = True
            break


def get_node_by_id(node_id):
    """Get a dialogue node by its ID"""
    for node in st.session_state.dialogue_data["dialogues"]:
        if node["id"] == node_id:
            return node
    return None


def get_response_by_id(node_id, response_id):
    """Get a response by its ID within a node"""
    node = get_node_by_id(node_id)
    if node:
        for resp in node["responses"]:
            if resp["id"] == response_id:
                return resp
    return None


def render_tree_view():
    """Render the dialogue tree overview"""
    st.header("Dialogue Tree")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Dialogue Nodes")
        for node in st.session_state.dialogue_data["dialogues"]:
            is_starting = st.session_state.dialogue_data["starting_dialogue"] == node["id"]
            is_selected = st.session_state.selected_node_id == node["id"]
            
            # Generate a label with status indicators
            label = node["id"]
            if is_starting:
                label = f"🚩 {label} (Starting Node)"
            
            # Create a selection button for each node
            if st.button(
                label, 
                key=f"select_{node['id']}", 
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.selected_node_id = node["id"]
                st.session_state.edit_mode = "node"
                st.experimental_rerun()
    
    with col2:
        st.subheader("Actions")
        
        if st.button("Add New Node", use_container_width=True):
            new_id = add_new_dialogue_node()
            st.session_state.selected_node_id = new_id
            st.session_state.edit_mode = "node"
            st.experimental_rerun()
        
        if st.session_state.selected_node_id:
            if st.button("Edit Selected Node", use_container_width=True):
                st.session_state.edit_mode = "node"
                st.experimental_rerun()
                
            # Set as starting node button
            if st.session_state.dialogue_data["starting_dialogue"] != st.session_state.selected_node_id:
                if st.button("Set as Starting Node", use_container_width=True):
                    st.session_state.dialogue_data["starting_dialogue"] = st.session_state.selected_node_id
                    st.session_state.modified = True
                    st.experimental_rerun()
            
            # Delete node button
            if st.button("Delete Selected Node", use_container_width=True, type="secondary"):
                if delete_node(st.session_state.selected_node_id):
                    st.success("Node deleted successfully")
                    st.experimental_rerun()


def render_node_editor():
    """Render the dialogue node editor"""
    node = get_node_by_id(st.session_state.selected_node_id)
    
    if not node:
        st.error("Selected node not found")
        st.session_state.edit_mode = "tree"
        st.experimental_rerun()
        return
    
    st.header(f"Edit Dialogue Node: {node['id']}")
    
    # Go back button
    if st.button("← Back to Tree View"):
        st.session_state.edit_mode = "tree"
        st.experimental_rerun()
    
    # Node editor form
    with st.form(key="node_editor"):
        # Basic node details
        new_npc_name = st.text_input("NPC Name", value=node["npc_name"])
        new_text = st.text_area("Dialogue Text", value=node["text"], height=150)
        
        # Show any other node properties here for editing
        
        if st.form_submit_button("Save Changes"):
            node["npc_name"] = new_npc_name
            node["text"] = new_text
            st.session_state.modified = True
            st.success("Node updated successfully")
    
    # Responses section
    st.subheader("Responses")
    
    if len(node["responses"]) == 0:
        st.info("This node has no responses. Add one below.")
    
    # Display existing responses
    for i, response in enumerate(node["responses"]):
        with st.expander(f"Response {i+1}: {response['text'][:30]}...", expanded=True):
            with st.form(key=f"response_editor_{i}"):
                new_response_text = st.text_area("Response Text", 
                                               value=response["text"], 
                                               key=f"response_text_{i}")
                
                # Dropdown for next dialogue selection
                next_dialogue_options = [("", "- Select -")] + [
                    (d["id"], f"{d['id']} ({d['npc_name']}: {d['text'][:20]}...)")
                    for d in st.session_state.dialogue_data["dialogues"]
                ]
                
                next_dialogue = st.selectbox(
                    "Next Dialogue", 
                    options=[o[0] for o in next_dialogue_options],
                    format_func=lambda x: next(o[1] for o in next_dialogue_options if o[0] == x),
                    index=next((idx for idx, o in enumerate(next_dialogue_options) if o[0] == response["next_dialogue"]), 0),
                    key=f"next_dialogue_{i}"
                )
                
                col1, col2 = st.columns(2)
                
                save_clicked = col1.form_submit_button("Save Response")
                delete_clicked = col2.form_submit_button("Delete Response", type="secondary")
                
                if save_clicked:
                    response["text"] = new_response_text
                    if next_dialogue:
                        response["next_dialogue"] = next_dialogue
                    st.session_state.modified = True
                    st.success("Response updated")
                
                if delete_clicked:
                    delete_response(node["id"], response["id"])
                    st.success("Response deleted")
                    st.experimental_rerun()
    
    # Add new response button
    if st.button("Add New Response"):
        add_response_to_node(node["id"])
        st.success("New response added")
        st.experimental_rerun()


def render_dialogue_preview():
    """Render a simple preview of the dialogue in action"""
    if not st.session_state.dialogue_loaded:
        return
    
    st.header("Preview")
    
    # Reset the preview to use the current dialogue data
    # This involves recreating the manager with the current data
    manager = DialogueManager()
    
    # Use a temporary file to store the dialogue data for testing
    temp_path = ".temp_dialogue_preview.json"
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.dialogue_data, f)
        
        success = manager.load_dialogue_file(temp_path)
        if success:
            # Display the current dialogue
            dialogue = manager.get_current_dialogue()
            if dialogue:
                st.markdown(f"**[{dialogue['npc_name']}]**")
                st.markdown(dialogue['text'])
                
                st.markdown("**Responses:**")
                for i, response in enumerate(dialogue["responses"], 1):
                    if st.button(response["text"], key=f"preview_response_{i}"):
                        manager.choose_response(response["id"])
                        st.experimental_rerun()
        else:
            st.error("Preview not available - dialogue has errors")
    except Exception as e:
        st.error(f"Error in preview: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


def render_dialogue_validator():
    """Render dialogue validation results"""
    st.header("Validation")
    
    # Create a temporary dialogue manager for validation
    manager = DialogueManager()
    
    # Create a temporary file to load
    temp_path = ".temp_dialogue_validation.json"
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.dialogue_data, f)
        
        success = manager.load_dialogue_file(temp_path)
        if success:
            errors = manager.validate_dialogue_tree()
            if errors:
                st.error("Validation failed")
                for error in errors:
                    st.warning(error)
            else:
                st.success("Dialogue tree is valid! No errors found.")
                
                # Additional statistics
                st.markdown("### Dialogue Statistics")
                num_nodes = len(st.session_state.dialogue_data["dialogues"])
                
                # Count total responses
                total_responses = sum(len(node["responses"]) for node in st.session_state.dialogue_data["dialogues"])
                
                # Identify terminal nodes (nodes with no responses)
                terminal_nodes = [node["id"] for node in st.session_state.dialogue_data["dialogues"] 
                                if len(node["responses"]) == 0]
                
                st.markdown(f"- **Total nodes:** {num_nodes}")
                st.markdown(f"- **Total responses:** {total_responses}")
                st.markdown(f"- **Terminal nodes:** {len(terminal_nodes)}")
                if terminal_nodes:
                    st.markdown("  Terminal node IDs:")
                    for node_id in terminal_nodes:
                        st.markdown(f"  - {node_id}")
        else:
            st.error("Validation failed - Unable to load dialogue data into manager")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Dialogue Editor",
        page_icon="✏️",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Application header
    st.title("Dialogue Tree Editor")
    
    # Sidebar for file operations
    with st.sidebar:
        st.header("File Operations")
        
        # Create new dialogue option
        if st.button("Create New Dialogue"):
            create_new_dialogue()
            st.success("New dialogue created")
            st.experimental_rerun()
        
        # Load existing dialogue
        st.subheader("Load Dialogue")
        
        # File selector for existing dialogues
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
                        if load_dialogue_file(selected_file):
                            st.success("Dialogue loaded successfully!")
                            st.session_state.edit_mode = "tree"
                            st.experimental_rerun()
                        else:
                            st.error("Failed to load dialogue. Check file format.")
        
        # Save dialogue option
        if st.session_state.dialogue_loaded:
            st.subheader("Save Dialogue")
            
            save_path = st.text_input("File path:", 
                                    value=f"../json/new_dialogue_{uuid.uuid4().hex[:6]}.json")
            
            if st.button("Save Dialogue", disabled=not st.session_state.modified):
                if save_dialogue_file(save_path):
                    st.success(f"Dialogue saved to {save_path}")
                else:
                    st.error("Failed to save dialogue")
        
        # View selection
        if st.session_state.dialogue_loaded:
            st.header("Views")
            
            view_options = {
                "tree": "Tree View",
                "node": "Node Editor",
                "preview": "Preview",
                "validate": "Validate"
            }
            
            selected_view = st.radio(
                "Select View",
                options=list(view_options.keys()),
                format_func=lambda x: view_options[x],
                index=list(view_options.keys()).index(st.session_state.edit_mode) 
                      if st.session_state.edit_mode in view_options else 0
            )
            
            if selected_view != st.session_state.edit_mode:
                st.session_state.edit_mode = selected_view
                st.experimental_rerun()
    
    # Main content area
    if not st.session_state.dialogue_loaded:
        st.info("Please create a new dialogue or load an existing dialogue file using the sidebar options.")
    else:
        # Render the appropriate view based on edit_mode
        if st.session_state.edit_mode == "tree":
            render_tree_view()
        elif st.session_state.edit_mode == "node":
            render_node_editor()
        elif st.session_state.edit_mode == "preview":
            render_dialogue_preview()
        elif st.session_state.edit_mode == "validate":
            render_dialogue_validator()


if __name__ == "__main__":
    main()