# Dialogue Tree System

A modular dialogue tree system for interactive storytelling and conversation simulations.

## Project Overview

This project creates a dialogue tree system with a flexible architecture consisting of three main components:

1. **Core Library** - The engine that handles dialogue logic, state management, and JSON parsing
2. **Streamlit UI** - A graphical web interface with retro terminal styling 
3. **Console UI** - A simple command-line interface for rapid testing and development

This separation allows for clean code organization, testability, and the ability to extend the system with new interfaces while maintaining the same core dialogue logic.

## Architecture

```
┌───────────────┐     ┌───────────────┐
│  Streamlit UI │     │   Console UI  │
└───────┬───────┘     └───────┬───────┘
        │                     │
        │   Imports & Uses    │
        └─────────┬───────────┘
                  │
                  ▼
         ┌─────────────────┐
         │   Core Library  │
         └────────┬────────┘
                  │
                  │  Loads & Parses
                  ▼
         ┌─────────────────┐
         │   JSON Files    │
         └─────────────────┘
```

## Component Requirements

### 1. Core Library (`dialogue_lib.py`)

- **Functions:**
  - Load and parse dialogue JSON files
  - Validate JSON structure and relationships
  - Track current dialogue state
  - Provide methods to get current dialogue text and response options
  - Process user choices and determine next dialogue
  - Handle any quest state if applicable

- **Requirements:**
  - Must be completely UI-agnostic
  - Should provide clean, documented API for UIs to consume
  - Must handle errors gracefully (malformed JSON, missing nodes, etc.)
  - Should implement proper dialogue traversal logic

### 2. Streamlit UI (`streamlit_app.py`)

- **Functions:**
  - Present retro terminal interface
  - Display current dialogue text and NPC name
  - Show clickable response options
  - Handle user interaction
  - Provide file upload functionality for custom dialogues
  - Display any quest information if applicable

- **Requirements:**
  - Must use the core library for all dialogue logic
  - Should handle responsive design
  - Must implement retro terminal aesthetics
  - Should provide clear user feedback

### 3. Console UI (`console_app.py`)

- **Functions:**
  - Text-based interface for dialogue display
  - Numbered menu for response selection
  - Simple dialogue navigation
  - Basic file loading capabilities

- **Requirements:**
  - Must use the same core library as the Streamlit UI
  - Should be minimalistic but fully functional
  - Must provide clear instruction text for users
  - Should work in any terminal environment

## JSON Dialogue Format

```json
{
  "starting_dialogue": "intro_1",
  
  "dialogues": [
    {
      "id": "intro_1",
      "npc_name": "Commander",
      "text": "Welcome aboard the station.",
      "responses": [
        {
          "id": "resp_1",
          "text": "Thanks, Commander.",
          "next_dialogue": "intro_2"
        },
        {
          "id": "resp_2",
          "text": "Where am I?",
          "next_dialogue": "location_info"
        }
      ]
    },
    // Additional dialogue nodes...
  ],
  
  "quests": [
    // Optional quest data...
  ]
}
```

## Project Structure

```
dialogue-system/
├── dialogue_lib.py              # Core dialogue library
├── streamlit_app.py             # Streamlit web interface
├── console_app.py               # Console interface
├── dialogues/                   # Dialogue JSON files
│   ├── example_dialogue.json    # Default dialogue
│   └── ...                      # Additional dialogues
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/dialogue-system.git
cd dialogue-system

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the console interface
python console_app.py

# Run the Streamlit interface
streamlit run streamlit_app.py
```

## Dependencies

- Python 3.7+
- Streamlit
- Json (standard library)
- Typing (standard library)

## Development Workflow

1. Develop and test core functionality in `dialogue_lib.py`
2. Use `console_app.py` for rapid testing of dialogue flow
3. Implement the full interface in `streamlit_app.py`
4. Create sample dialogue trees in the JSON format
5. Test with different dialogue files and edge cases
