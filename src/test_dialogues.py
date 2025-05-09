"""
Test script for dialogue files.
"""
from dialogue_lib import DialogueManager


def test_dialogue_file(file_path):
    """Test a dialogue file by loading it and checking for errors."""
    print(f"\nTesting dialogue file: {file_path}")
    manager = DialogueManager()
    success = manager.load_dialogue_file(file_path)
    
    if not success:
        print("Failed to load dialogue file!")
        return
    
    print("Dialogue loaded successfully!")
    
    # Validate the dialogue tree
    errors = manager.validate_dialogue_tree()
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Dialogue tree is valid. No errors found.")
    
    # Display the first dialogue
    dialogue = manager.get_current_dialogue()
    if dialogue:
        print(f"\nStarting Dialogue: {dialogue['id']}")
        print(f"NPC: {dialogue['npc_name']}")
        print(f"Text: {dialogue['text'][:100]}..." if len(dialogue['text']) > 100 else f"Text: {dialogue['text']}")
        print(f"Number of responses: {len(dialogue['responses'])}")
    else:
        print("Could not get starting dialogue!")


# Test all dialogue files
test_dialogue_file("../json/example-dialogue-json.json")
test_dialogue_file("../json/dialogue_tutorial_simplified.json")
test_dialogue_file("../json/dialogue_escape_simplified.json")