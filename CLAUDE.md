# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project is a dialogue tree system that allows users to create, load, and navigate text-based conversation trees. It features:

- A core library for managing dialogue trees stored in JSON format
- Multiple UI options including a console interface and Streamlit web interface 
- Support for branching conversations

## Development Approach

The project follows an iterative approach with two main development phases:

1. **MVP Implementation** (Current Version):
   - Core library with basic functionality
   - Simple console interface
   - Basic Streamlit web interface
   - Support for branching dialogues

2. **Full Implementation** (Future Work):
   - Quest system tracking
   - Script commands for triggering events
   - Enhanced styling options
   - Complete dialogue history view

## Repository Structure

- `/src/`: Core implementation files
  - `dialogue_lib.py`: Core dialogue management functionality
  - `console_app.py`: Text-based console interface
  - `streamlit_app.py`: Web-based UI built with Streamlit
- `/json/`: Example dialogue files in JSON format
- `/docs/`: Design documents and specifications

## Commands

### Running the Applications

To run the console application:
```bash
cd src
python console_app.py
```

To run the Streamlit application (requires Streamlit installed):
```bash
cd src
streamlit run streamlit_app.py
```

### Installing Dependencies

```bash
pip install streamlit
```

## Development Notes

The system follows a modular design with three main components:

1. **Core Library (`dialogue_lib.py`)**: Handles all dialogue logic independently of UI
   - Loading and parsing dialogue JSON files
   - Dialogue traversal and state management
   - Validation of dialogue trees

2. **Console UI (`console_app.py`)**: Simple text-based interface for testing
   - Shows dialogue with numbered responses
   - Provides reset and exit options

3. **Streamlit UI (`streamlit_app.py`)**: More polished web interface
   - File selection
   - Styled dialogue display
   - Clickable response buttons
   - Dialogue history

The system uses JSON files to store dialogue trees. Each dialogue has an ID, NPC name, text, and a list of possible responses. Each response has an ID, text, and the ID of the next dialogue to navigate to.

When enhancing the system, maintain this clean separation between the core library and UI layers.

## Next Development Steps

For the next phase of development (moving beyond MVP), focus on these key areas:

1. **Implement Quest System**:
   - Enhance `dialogue_lib.py` to fully support the quest tracking system
   - Add the handling of script commands for quest updates
   - Implement the `get_active_quests` functionality

2. **Expand Validation**:
   - Enhance the `validate_dialogue_tree` method to check quest references
   - Add more comprehensive validation for dialogue structure
   - Implement validation reporting in the UI

3. **UI Enhancements**:
   - Add retro terminal styling to the Streamlit interface
   - Implement the debug information panel
   - Add quest display to both UI interfaces
   - Add file upload functionality to Streamlit

4. **Testing and Documentation**:
   - Create comprehensive test cases
   - Add more example dialogue files
   - Enhance documentation with user guides