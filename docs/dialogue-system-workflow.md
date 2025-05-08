# Dialogue System Development Workflow

This guide outlines the recommended development workflow for creating the dialogue system, focusing on incremental development and testing.

## Initial Setup

1. **Create the project structure**
   ```
   dialogue-system/
   ├── dialogue_lib.py
   ├── console_app.py
   ├── streamlit_app.py
   ├── dialogues/
   │   └── example_dialogue.json
   └── requirements.txt
   ```

2. **Set up your development environment**
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate it (Windows)
   venv\Scripts\activate
   
   # Activate it (macOS/Linux)
   source venv/bin/activate
   
   # Install dependencies
   pip install streamlit
   ```

3. **Create a simple example JSON dialogue file**
   Create a basic dialogue tree in `dialogues/example_dialogue.json` with a few nodes to test with.

## Development Approach

### Step 1: Core Library First

Start by implementing the core dialogue library:

1. Create the `DialogueManager` class in `dialogue_lib.py`
2. Implement basic JSON loading functionality
3. Add dialogue traversal logic (current dialogue, response handling)
4. Create a small test script to verify functionality
5. Test manually with your example dialogue file

**Key Milestone**: The core library should be able to load a dialogue file, navigate between nodes, and track the current state without any UI dependencies.

### Step 2: Console UI Development

Build the console interface to test your dialogue system:

1. Create the basic console application structure
2. Connect it to your core library
3. Implement the text-based dialogue display
4. Add numbered response selection
5. Test with your example dialogue

**Key Milestone**: You should be able to navigate through your dialogue tree using the console interface.

### Step 3: Streamlit UI Basics

Create the foundation for your Streamlit interface:

1. Set up the basic Streamlit app
2. Connect it to your core library
3. Implement simple dialogue display
4. Add response buttons
5. Ensure navigation works correctly

**Key Milestone**: At this point, you should have a functional MVP with both console and Streamlit interfaces.

### Step 4: Add Core Features

Enhance the system with key functionality:

1. Add dialogue history tracking
2. Implement quest system
3. Add dialogue tree validation
4. Improve error handling

### Step 5: UI Enhancement

Polish your interfaces:

1. Add retro terminal styling to Streamlit
2. Implement dialogue history display
3. Add file selection/upload functionality
4. Create debug view for development

### Step 6: Documentation and Testing

Finalize your system:

1. Add comprehensive comments
2. Create additional example dialogue files
3. Test with edge cases
4. Optimize performance for larger dialogue trees

## Development Tips

### Incremental Testing

- **Test each component in isolation**: Verify core library functionality before connecting UIs
- **Create simple dialogue files first**: Start with minimal dialogue trees and progressively add complexity
- **Add one feature at a time**: Implement, test, then move to the next feature

### Common Pitfalls to Avoid

1. **Complex data structures**: Keep your JSON format straightforward at first
2. **UI-dependent logic**: Maintain clear separation between core functionality and UI
3. **Deep nesting**: Avoid deeply nested dialogue trees until basic navigation works
4. **Premature optimization**: Focus on functionality first, then optimize

### Development Cycle

For each feature:

1. **Design**: Plan how the feature will work and integrate with existing code
2. **Implement**: Write the code for the feature
3. **Test**: Verify it works as expected
4. **Refine**: Clean up the code and fix any issues
5. **Document**: Add comments and update documentation

## JSON Format Evolution

Start with a simple format and evolve as needed:

### Basic Format (Start with this)
```json
{
  "starting_dialogue": "intro_1",
  "dialogues": [
    {
      "id": "intro_1",
      "npc_name": "NPC",
      "text": "Hello there!",
      "responses": [
        {
          "id": "resp_1",
          "text": "Hi",
          "next_dialogue": "intro_2"
        }
      ]
    }
  ]
}
```

### Enhanced Format (Add later)
```json
{
  "starting_dialogue": "intro_1",
  "dialogues": [
    {
      "id": "intro_1",
      "npc_name": "NPC",
      "text": "Hello there!",
      "responses": [
        {
          "id": "resp_1",
          "text": "Hi",
          "next_dialogue": "intro_2",
          "script": [
            {
              "type": "start_quest",
              "quest_id": "main_quest"
            }
          ]
        }
      ]
    }
  ],
  "quests": [
    {
      "id": "main_quest",
      "name": "The Main Quest",
      "stages": [
        {
          "id": "stage_1",
          "journal_entry": "I've started the main quest."
        }
      ]
    }
  ]
}
```

## Getting Started

1. Begin by implementing the basic `dialogue_lib.py` functionality
2. Create a simple example dialogue JSON file
3. Use the console application to test your implementation
4. Once the core functionality works, move on to the Streamlit interface

This incremental approach ensures you have a working system at each stage of development.
