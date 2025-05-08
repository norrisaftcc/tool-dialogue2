# Dialogue System Component Design

## 1. Core Library (`dialogue_lib.py`)

This is the heart of our system, providing all dialogue logic independent of UI.

```python
"""
Dialogue Tree Library - Core functionality for dialogue tree management.
"""
import json
from typing import Dict, List, Any, Optional, Tuple


class DialogueManager:
    def __init__(self):
        self.dialogues: Dict = {}
        self.quests: Dict = {}
        self.current_dialogue_id: str = ""
        self.starting_dialogue_id: str = ""
        self.active_quests: Dict = {}
    
    def load_dialogue_file(self, file_path: str) -> bool:
        """
        Load a dialogue JSON file and validate its structure.
        
        Args:
            file_path: Path to the JSON dialogue file
            
        Returns:
            bool: True if loading succeeded, False otherwise
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Validate required fields
            if "starting_dialogue" not in data or "dialogues" not in data:
                print("Error: Invalid dialogue file structure")
                return False
                
            # Store dialogue data
            self.dialogues = {d["id"]: d for d in data["dialogues"]}
            self.starting_dialogue_id = data["starting_dialogue"]
            self.current_dialogue_id = self.starting_dialogue_id
            
            # Store quest data if present
            if "quests" in data:
                self.quests = {q["id"]: q for q in data["quests"]}
            
            return True
            
        except Exception as e:
            print(f"Error loading dialogue file: {e}")
            return False
    
    def load_dialogue_from_string(self, json_string: str) -> bool:
        """
        Load dialogue data directly from a JSON string.
        Useful for web interfaces with file upload.
        """
        try:
            data = json.loads(json_string)
            
            # Validate required fields
            if "starting_dialogue" not in data or "dialogues" not in data:
                print("Error: Invalid dialogue file structure")
                return False
                
            # Store dialogue data
            self.dialogues = {d["id"]: d for d in data["dialogues"]}
            self.starting_dialogue_id = data["starting_dialogue"]
            self.current_dialogue_id = self.starting_dialogue_id
            
            # Store quest data if present
            if "quests" in data:
                self.quests = {q["id"]: q for q in data["quests"]}
            
            return True
            
        except Exception as e:
            print(f"Error parsing dialogue JSON: {e}")
            return False
    
    def reset_dialogue(self) -> None:
        """Reset to the starting dialogue"""
        self.current_dialogue_id = self.starting_dialogue_id
    
    def get_current_dialogue(self) -> Optional[Dict]:
        """
        Get the current dialogue node with its text and responses.
        
        Returns:
            Dict containing dialogue information or None if invalid
        """
        if not self.current_dialogue_id or self.current_dialogue_id not in self.dialogues:
            return None
        
        return self.dialogues[self.current_dialogue_id]
    
    def choose_response(self, response_id: str) -> Tuple[bool, Optional[str]]:
        """
        Process a user's response choice and update the current dialogue.
        
        Args:
            response_id: The ID of the selected response
            
        Returns:
            (success, quest_update): 
            - success: Whether the response was valid
            - quest_update: ID of any quest that was updated, if applicable
        """
        dialogue = self.get_current_dialogue()
        if not dialogue:
            return False, None
        
        # Find the response with the given ID
        for response in dialogue["responses"]:
            if response["id"] == response_id:
                # Update current dialogue
                self.current_dialogue_id = response["next_dialogue"]
                
                # Check for script commands (like quest updates)
                quest_update = None
                if "script" in response and response["script"]:
                    for cmd in response["script"]:
                        if cmd.get("type") == "start_quest" and "quest_id" in cmd:
                            quest_id = cmd["quest_id"]
                            self.active_quests[quest_id] = {"current_stage": 0}
                            quest_update = quest_id
                        
                        elif cmd.get("type") == "advance_quest" and "quest_id" in cmd:
                            quest_id = cmd["quest_id"]
                            if quest_id in self.active_quests:
                                self.active_quests[quest_id]["current_stage"] += 1
                                quest_update = quest_id
                
                return True, quest_update
        
        return False, None
    
    def get_active_quests(self) -> List[Dict]:
        """
        Get information about all active quests.
        
        Returns:
            List of quest information dictionaries
        """
        active_quest_info = []
        
        for quest_id, status in self.active_quests.items():
            if quest_id in self.quests:
                quest = self.quests[quest_id]
                current_stage = status["current_stage"]
                
                # Get current stage info
                stage_info = None
                if "stages" in quest and len(quest["stages"]) > current_stage:
                    stage_info = quest["stages"][current_stage]
                
                active_quest_info.append({
                    "id": quest_id,
                    "name": quest.get("name", quest_id),
                    "current_stage": current_stage,
                    "stage_info": stage_info
                })
        
        return active_quest_info
    
    def validate_dialogue_tree(self) -> List[str]:
        """
        Validate the entire dialogue tree for errors.
        
        Returns:
            List of error messages, empty if no errors
        """
        errors = []
        
        # Check if starting dialogue exists
        if self.starting_dialogue_id not in self.dialogues:
            errors.append(f"Starting dialogue '{self.starting_dialogue_id}' not found")
        
        # Check all referenced dialogues exist
        for dialogue_id, dialogue in self.dialogues.items():
            for response in dialogue.get("responses", []):
                next_dialogue = response.get("next_dialogue")
                if next_dialogue and next_dialogue not in self.dialogues:
                    errors.append(
                        f"Dialogue '{dialogue_id}' references non-existent dialogue '{next_dialogue}'"
                    )
        
        # Check quest references
        for dialogue_id, dialogue in self.dialogues.items():
            for response in dialogue.get("responses", []):
                if "script" in response:
                    for cmd in response["script"]:
                        if ("type" in cmd and cmd["type"] in ["start_quest", "advance_quest"] 
                                and "quest_id" in cmd):
                            quest_id = cmd["quest_id"]
                            if quest_id not in self.quests:
                                errors.append(
                                    f"Dialogue '{dialogue_id}' references non-existent quest '{quest_id}'"
                                )
        
        return errors


# Simple usage example
if __name__ == "__main__":
    # Test the library functionality
    manager = DialogueManager()
    success = manager.load_dialogue_file("dialogues/example_dialogue.json")
    
    if success:
        print("Dialogue loaded successfully.")
        
        # Validate dialogue tree
        errors = manager.validate_dialogue_tree()
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"- {error}")
        else:
            print("Dialogue tree is valid.")
        
        # Get first dialogue
        dialogue = manager.get_current_dialogue()
        print(f"\n{dialogue['npc_name']}: {dialogue['text']}")
        
        for i, response in enumerate(dialogue["responses"], 1):
            print(f"{i}. {response['text']}")
    else:
        print("Failed to load dialogue.")
```

## 2. Console UI (`console_app.py`)

A simple text-based interface for testing dialogue flow.

```python
"""
Console Interface for Dialogue Tree System.
A simple text-based UI for testing dialogue trees.
"""
import os
import sys
from dialogue_lib import DialogueManager


def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the application header"""
    print("=" * 60)
    print("                DIALOGUE TREE CONSOLE INTERFACE               ")
    print("=" * 60)
    print()


def print_dialogue(dialogue):
    """Print the current dialogue with formatting"""
    if not dialogue:
        print("Error: No active dialogue")
        return
    
    print(f"\n[{dialogue['npc_name']}]")
    print(f"{dialogue['text']}")
    print("\nResponses:")
    
    for i, response in enumerate(dialogue["responses"], 1):
        print(f"{i}. {response['text']}")


def print_quests(quests):
    """Print active quests"""
    if not quests:
        return
    
    print("\n--- ACTIVE QUESTS ---")
    for quest in quests:
        print(f"* {quest['name']}")
        if quest.get("stage_info") and "journal_entry" in quest["stage_info"]:
            print(f"  {quest['stage_info']['journal_entry']}")
    print("--------------------\n")


def main():
    """Main console application"""
    manager = DialogueManager()
    
    # Default dialogue file
    default_file = "dialogues/example_dialogue.json"
    
    # Welcome message and file selection
    clear_screen()
    print_header()
    print("Welcome to the Dialogue Tree Console Interface!")
    print("\nEnter the path to a dialogue JSON file, or press Enter for default:")
    
    file_path = input(f"[{default_file}]: ").strip()
    if not file_path:
        file_path = default_file
    
    # Load the dialogue file
    if not manager.load_dialogue_file(file_path):
        print(f"Error: Failed to load dialogue file '{file_path}'")
        print("Please check the file path and JSON structure.")
        input("\nPress Enter to exit...")
        return
    
    # Main dialogue loop
    while True:
        clear_screen()
        print_header()
        
        # Get and display current dialogue
        dialogue = manager.get_current_dialogue()
        
        if not dialogue:
            print("Error: Invalid dialogue state. Resetting to start.")
            manager.reset_dialogue()
            dialogue = manager.get_current_dialogue()
        
        # Display active quests
        quests = manager.get_active_quests()
        if quests:
            print_quests(quests)
        
        # Display dialogue
        print_dialogue(dialogue)
        
        # Get user input
        print("\nEnter response number, 'r' to reset, or 'q' to quit:")
        choice = input("> ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 'r':
            manager.reset_dialogue()
            continue
        
        # Process numbered choice
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(dialogue["responses"]):
                response = dialogue["responses"][choice_num - 1]
                success, quest_update = manager.choose_response(response["id"])
                
                if not success:
                    print("Error processing response. Please try again.")
                    input("Press Enter to continue...")
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
        except ValueError:
            print("Please enter a valid number, 'r', or 'q'.")
            input("Press Enter to continue...")
    
    print("\nThank you for using the Dialogue Tree Console Interface!")


if __name__ == "__main__":
    main()
```

## 3. Streamlit UI (`streamlit_app.py`)

A graphical web interface with retro terminal styling.

```python
"""
Streamlit Interface for Dialogue Tree System.
A retro terminal-style UI for interactive dialogue trees.
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
    
    if "show_debug" not in st.session_state:
        st.session_state.show_debug = False


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


def load_dialogue_from_upload(uploaded_file):
    """Load dialogue from uploaded file"""
    try:
        content = uploaded_file.getvalue().decode("utf-8")
        success = st.session_state.manager.load_dialogue_from_string(content)
        
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
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return False


def handle_response(response_id):
    """Handle user response selection"""
    success, quest_update = st.session_state.manager.choose_response(response_id)
    
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
        page_title="Retro Terminal Dialogue System",
        page_icon="🖥️",
        layout="centered"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Custom CSS for retro terminal look
    st.markdown("""
    <style>
        .terminal {
            background-color: #000000;
            color: #00FF00;
            font-family: 'Courier New', monospace;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        
        .terminal-header {
            border-bottom: 1px solid #00FF00;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }
        
        .npc-name {
            font-weight: bold;
            color: #FFFF00;
        }
        
        .response-btn {
            background-color: #003300;
            color: #00FF00;
            border: 1px solid #00FF00;
            margin: 5px 0;
            text-align: left;
            cursor: pointer;
            width: 100%;
        }
        
        .response-btn:hover {
            background-color: #004400;
        }
        
        .quest-box {
            background-color: #002200;
            border: 1px dashed #00FF00;
            padding: 10px;
            margin: 10px 0;
        }
        
        .history-box {
            border-bottom: 1px dotted #006600;
            opacity: 0.8;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }
        
        /* Override some Streamlit styles for better terminal look */
        .stButton>button {
            background-color: #003300;
            color: #00FF00;
            border: 1px solid #00FF00;
        }
        
        .stButton>button:hover {
            background-color: #004400;
            color: #00FF00;
            border: 1px solid #00FF00;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Application header
    st.markdown('<div class="terminal-header"><h1>Retro Terminal Dialogue System</h1></div>', unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown('<div class="terminal-header"><h3>Controls</h3></div>', unsafe_allow_html=True)
        
        # File loading options
        st.markdown("### Load Dialogue File")
        
        # Default files
        dialogue_dir = "dialogues"
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
        
        # File upload
        st.markdown("### Or Upload a File")
        uploaded_file = st.file_uploader("Upload JSON dialogue file:", type=["json"])
        
        if uploaded_file is not None:
            if st.button("Load Uploaded File"):
                with st.spinner("Loading dialogue..."):
                    if load_dialogue_from_upload(uploaded_file):
                        st.success("Dialogue loaded successfully!")
                    else:
                        st.error("Failed to load dialogue. Check file format.")
        
        # Reset button
        if st.session_state.dialogue_loaded:
            if st.button("Reset Dialogue"):
                reset_dialogue()
        
        # Debug toggle
        st.markdown("### Debug Options")
        st.checkbox("Show Debug Info", key="show_debug")
    
    # Main content area
    if not st.session_state.dialogue_loaded:
        st.markdown(
            '<div class="terminal">'
            '<p>Welcome to the Retro Terminal Dialogue System.</p>'
            '<p>Please load a dialogue file using the sidebar options.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        # Display terminal interface
        st.markdown('<div class="terminal">', unsafe_allow_html=True)
        
        # Display quest information
        quests = st.session_state.manager.get_active_quests()
        if quests:
            quest_html = '<div class="quest-box"><h3>Active Quests:</h3>'
            for quest in quests:
                quest_html += f'<p>• {quest["name"]}</p>'
                if quest.get("stage_info") and "journal_entry" in quest["stage_info"]:
                    quest_html += f'<p style="margin-left: 15px;">{quest["stage_info"]["journal_entry"]}</p>'
            quest_html += '</div>'
            st.markdown(quest_html, unsafe_allow_html=True)
        
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
                f'<span class="npc-name">[{current["npc_name"]}]</span><br>'
                f'{current["text"]}',
                unsafe_allow_html=True
            )
            
            # Display response options
            st.markdown('<div style="margin-top: 20px;"><h4>Your Response:</h4></div>', unsafe_allow_html=True)
            
            for response in st.session_state.current_dialogue["responses"]:
                if st.button(response["text"], key=response["id"], help=response["id"]):
                    handle_response(response["id"])
                    st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Debug information
        if st.session_state.show_debug:
            with st.expander("Debug Information"):
                st.write("Current Dialogue ID:", st.session_state.manager.current_dialogue_id)
                st.write("All Dialogues:", st.session_state.manager.dialogues)
                st.write("Active Quests:", st.session_state.manager.active_quests)
                errors = st.session_state.manager.validate_dialogue_tree()
                st.write("Validation Errors:", errors if errors else "None")


if __name__ == "__main__":
    main()
```

## Sample JSON Dialogue File (`dialogues/example_dialogue.json`)

```json
{
  "starting_dialogue": "intro_1",
  
  "dialogues": [
    {
      "id": "intro_1",
      "npc_name": "Commander",
      "text": "Welcome aboard the Stellar Station. I'm Commander Shepard, and we're facing a critical situation that requires your expertise.",
      "responses": [
        {
          "id": "resp_1",
          "text": "Thanks, Commander. What's the situation?",
          "next_dialogue": "mission_brief"
        },
        {
          "id": "resp_2",
          "text": "Where am I? How did I get here?",
          "next_dialogue": "location_info"
        }
      ]
    },
    {
      "id": "mission_brief",
      "npc_name": "Commander",
      "text": "Our station's main reactor is failing. Without repairs, we'll lose life support in 12 hours. You're the only engineer qualified to fix it.",
      "responses": [
        {
          "id": "resp_3",
          "text": "I'll help. What do I need to do?",
          "next_dialogue": "task_info",
          "script": [
            {
              "type": "start_quest",
              "quest_id": "reactor_repair"
            }
          ]
        },
        {
          "id": "resp_4",
          "text": "Why me? Don't you have other engineers?",
          "next_dialogue": "why_you"
        }
      ]
    },
    {
      "id": "location_info",
      "npc_name": "Commander",
      "text": "You're aboard the Stellar Station, humanity's furthest outpost in the Tau Ceti system. You arrived yesterday on the transport ship after volunteering for our engineering program.",
      "responses": [
        {
          "id": "resp_5",
          "text": "I remember now. Tell me about the situation.",
          "next_dialogue": "mission_brief"
        },
        {
          "id": "resp_6",
          "text": "I need a moment to process this.",
          "next_dialogue": "take_time"
        }
      ]
    },
    {
      "id": "why_you",
      "npc_name": "Commander",
      "text": "Our chief engineer was injured in the initial malfunction. The other staff don't have your specialized knowledge of quantum containment systems. We reviewed your credentials - you've fixed similar problems before.",
      "responses": [
        {
          "id": "resp_7",
          "text": "Alright, I understand. I'll help.",
          "next_dialogue": "task_info",
          "script": [
            {
              "type": "start_quest",
              "quest_id": "reactor_repair"
            }
          ]
        },
        {
          "id": "resp_8",
          "text": "I need more information about the reactor first.",
          "next_dialogue": "reactor_info"
        }
      ]
    },
    {
      "id": "take_time",
      "npc_name": "Commander",
      "text": "I understand this is a lot to take in. Unfortunately, we don't have much time. The station's reactor is failing, and we need your help.",
      "responses": [
        {
          "id": "resp_9",
          "text": "Tell me more about this reactor problem.",
          "next_dialogue": "mission_brief"
        }
      ]
    },
    {
      "id": "reactor_info",
      "npc_name": "Commander",
      "text": "It's a standard Mark VII Quantum Fusion Reactor, but with customized coolant systems for deep space operation. The containment field is fluctuating and we're seeing dangerous radiation spikes in sectors 7 through 9.",
      "responses": [
        {
          "id": "resp_10",
          "text": "I see the problem. Let's get started.",
          "next_dialogue": "task_info",
          "script": [
            {
              "type": "start_quest",
              "quest_id": "reactor_repair"
            }
          ]
        }
      ]
    },
    {
      "id": "task_info",
      "npc_name": "Commander",
      "text": "You'll need to stabilize the containment field first, then repair the coolant systems. Security Officer Chen will escort you to the reactor room. Be careful - radiation levels are high.",
      "responses": [
        {
          "id": "resp_11",
          "text": "I'll need protective gear and tools.",
          "next_dialogue": "equipment"
        },
        {
          "id": "resp_12",
          "text": "Let's not waste time. Take me there now.",
          "next_dialogue": "to_reactor",
          "script": [
            {
              "type": "advance_quest",
              "quest_id": "reactor_repair"
            }
          ]
        }
      ]
    },
    {
      "id": "equipment",
      "npc_name": "Commander",
      "text": "Of course. We've prepared a Rad-X suit for you and a specialized toolkit is waiting in the prep room. Officer Chen will help you gear up before heading to the reactor.",
      "responses": [
        {
          "id": "resp_13",
          "text": "Thanks. I'm ready when you are.",
          "next_dialogue": "to_reactor",
          "script": [
            {
              "type": "advance_quest",
              "quest_id": "reactor_repair"
            }
          ]
        }
      ]
    },
    {
      "id": "to_reactor",
      "npc_name": "Security Officer Chen",
      "text": "Follow me to the reactor room. Stay close - we've had to seal off several corridors due to radiation leaks. The situation is getting worse by the hour.",
      "responses": [
        {
          "id": "resp_14",
          "text": "Tell me what you've observed with the reactor.",
          "next_dialogue": "chen_observations"
        },
        {
          "id": "resp_15",
          "text": "Let's hurry. Time is critical.",
          "next_dialogue": "reactor_arrival"
        }
      ]
    },
    {
      "id": "chen_observations",
      "npc_name": "Security Officer Chen",
      "text": "I'm no engineer, but I've seen the coolant pipes vibrating violently before they ruptured. The control terminals are showing all kinds of errors, and there's a strange humming sound coming from the core chamber.",
      "responses": [
        {
          "id": "resp_16",
          "text": "That helps. Let's get to the reactor room.",
          "next_dialogue": "reactor_arrival"
        }
      ]
    },
    {
      "id": "reactor_arrival",
      "npc_name": "Security Officer Chen",
      "text": "Here we are. The reactor control room. You can access the core from that terminal. I'll stand guard, but I can't stay long due to radiation exposure. Good luck - we're all counting on you.",
      "responses": [
        {
          "id": "resp_17",
          "text": "I'll do my best. Let me get to work.",
          "next_dialogue": "ending"
        }
      ]
    },
    {
      "id": "ending",
      "npc_name": "System",
      "text": "End of demo dialogue. In a full game, you would now begin the reactor repair sequence.",
      "responses": [
        {
          "id": "resp_18",
          "text": "Return to the beginning",
          "next_dialogue": "intro_1"
        }
      ]
    }
  ],
  
  "quests": [
    {
      "id": "reactor_repair",
      "name": "Repair the Stellar Station Reactor",
      "stages": [
        {
          "id": "stage_1",
          "journal_entry": "I need to meet with Officer Chen and head to the reactor room."
        },
        {
          "id": "stage_2",
          "journal_entry": "I've arrived at the reactor room. Now I need to stabilize the containment field and repair the coolant system."
        }
      ]
    }
  ]
}
```

## Usage Instructions

1. **Save all three files** in your project directory
2. **Create a dialogues folder** and save the example dialogue JSON file there
3. **Install dependencies:**
   ```bash
   pip install streamlit
   ```
4. **Run the console interface first** to test your dialogue:
   ```bash
   python console_app.py
   ```
5. **Run the Streamlit interface** for the full experience:
   ```bash
   streamlit run streamlit_app.py
   ```

The components all work together while maintaining clean separation:
- `dialogue_lib.py` handles all dialogue logic and state management
- `console_app.py` provides quick testing through a simple interface
- `streamlit_app.py` delivers the full retro terminal experience

This modular design allows you to modify each component independently without affecting the others.
