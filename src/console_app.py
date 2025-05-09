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


def main():
    """Main console application"""
    manager = DialogueManager()
    
    # Default dialogue file
    default_file = "../json/example-dialogue-json.json"
    
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
    
    # Validate dialogue tree
    errors = manager.validate_dialogue_tree()
    if errors:
        print("Warning: Dialogue tree has validation errors:")
        for error in errors:
            print(f"- {error}")
        print("\nContinuing anyway, but some paths may not work correctly.")
        input("Press Enter to continue...")
    
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
                success = manager.choose_response(response["id"])
                
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