# Dialogue Tree System

A simple yet flexible system for creating, loading, and navigating text-based conversation trees with multiple UI options.

## Features

- **Core Dialogue Library**: Load JSON dialogue files, navigate between nodes, validate dialogue structure
- **Console Interface**: Text-based dialogue display with numbered responses
- **Streamlit Interface**: Web-based UI with dialogue history and interactive response buttons
- **Dialogue Editor**: Visual editor for creating and modifying dialogue trees
- **Branching Conversations**: Create complex dialogue trees with multiple paths

## Project Understanding

- The dialogue system uses a tree structure for organizing conversations
- Each dialogue node contains text, speaker information, and possible responses
- Responses determine the path through the conversation tree
- Modular design separates core functionality from UI implementations

<img src="docs/dialogue-tree-diagram-svg.svg" width="500">

*sample dialogue tree*

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Streamlit (for web interface only): `pip install streamlit`

### Running the Applications

1. **Console Interface**

   ```bash
   cd src
   python console_app.py
   ```

2. **Streamlit Interface**

   ```bash
   cd src
   streamlit run streamlit_app.py
   ```

3. **Dialogue Editor**

   ```bash
   cd src
   streamlit run editor_app.py
   ```
   
   The dialogue editor provides a visual interface for creating and editing dialogue trees:
   
   - **Tree View**: Overview of all dialogue nodes with add/edit/delete functionality
   - **Node Editor**: Modify dialogue text, NPC names, and manage responses
   - **Preview**: Test your dialogue tree interactively
   - **Validation**: Check for errors and view statistics about your dialogue tree

## Creating Dialogue Files

Dialogue trees can be created using the dialogue editor or manually defined in JSON files with the following structure:

```json
{
  "starting_dialogue": "intro_id",
  "dialogues": [
    {
      "id": "intro_id",
      "npc_name": "Character Name",
      "text": "This is what the character says.",
      "responses": [
        {
          "id": "resp_1",
          "text": "Player response option 1",
          "next_dialogue": "next_dialogue_id_1"
        },
        {
          "id": "resp_2",
          "text": "Player response option 2",
          "next_dialogue": "next_dialogue_id_2"
        }
      ]
    },
    {
      "id": "next_dialogue_id_1",
      "npc_name": "Character Name",
      "text": "Response to the first option.",
      "responses": [
        // More responses...
      ]
    }
    // More dialogue nodes...
  ]
}
```

See the example in `json/example-dialogue-json.json` for a complete dialogue tree.

## Project Structure

- `src/dialogue_lib.py`: Core dialogue management functionality
- `src/console_app.py`: Text-based console interface
- `src/streamlit_app.py`: Web-based UI built with Streamlit
- `src/editor_app.py`: Visual dialogue editor built with Streamlit
- `json/`: Example dialogue files
- `docs/`: Design documents and technical specs

## Using the Dialogue Editor

The dialogue editor allows you to create and modify dialogue trees through a user-friendly interface.

### Key Features

1. **Creation & Editing**
   - Create new dialogue trees from scratch
   - Load and edit existing dialogue JSON files
   - Add, edit, and delete dialogue nodes
   - Add, edit, and delete responses
   - Connect responses to different dialogue nodes

2. **Visual Tools**
   - Tree view showing all dialogue nodes
   - Node editor for modifying dialogue text and NPC names
   - Response management with connections to other nodes
   - Validation view to check for errors

3. **Testing**
   - Live preview to test the dialogue flow
   - Validation to identify errors in the dialogue structure

### Workflow

1. **Create or Load a Dialogue Tree**
   - Click "Create New Dialogue" to start from scratch
   - Or select an existing JSON file from the dropdown

2. **Edit Dialogue Nodes**
   - Use Tree View to see all nodes
   - Click on a node to edit its content
   - Add responses to connect to other dialogue nodes
   - Set a node as the starting point of the dialogue

3. **Test Your Dialogue**
   - Use Preview mode to test dialogue flow
   - Validate your dialogue tree to check for errors
   - View statistics about your dialogue tree

4. **Save Your Work**
   - Enter a file path in the sidebar
   - Click "Save Dialogue" to export to JSON

## Development Approach

The project follows an iterative approach:

1. **MVP Implementation**:
   - Core library with basic functionality
   - Simple console interface
   - Basic Streamlit web interface
   - Support for branching dialogues

2. **Current Version**:
   - All MVP features
   - Visual dialogue editor
   - Dialogue validation
   - Multiple example dialogues
   
3. **Full Implementation** (Future Sprints):
   - Quest system tracking
   - Script commands for triggering events
   - Enhanced styling options
   - Complete dialogue history view
   - Comprehensive validation

## Development Workflow

1. **Set up the project structure** ✓
2. **Implement the core library** ✓
3. **Create the console interface** ✓
4. **Build the Streamlit interface** ✓
5. **Test with example dialogues** ✓
6. **Add advanced features**
7. **Polish UI and user experience**
8. **Comprehensive testing**

## License

This project is licensed under the MIT License - see the LICENSE file for details.
