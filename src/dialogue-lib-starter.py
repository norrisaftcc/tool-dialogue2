"""
Dialogue Tree Library - Core functionality for dialogue tree management.

This module provides the foundation for loading, parsing, and traversing
dialogue trees stored in JSON format.
"""
import json
from typing import Dict, List, Any, Optional, Tuple


class DialogueManager:
    """Manages dialogue trees and state."""
    
    def __init__(self):
        """Initialize the dialogue manager."""
        # Dictionary to store all dialogues, keyed by ID
        self.dialogues: Dict = {}
        
        # Dictionary to store all quests, keyed by ID
        self.quests: Dict = {}
        
        # ID of the current active dialogue
        self.current_dialogue_id: str = ""
        
        # ID of the starting dialogue
        self.starting_dialogue_id: str = ""
        
        # Track active quests and their state
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
            with open(file_path, 'r', encoding='utf-8') as f:
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
            else:
                self.quests = {}
                
            self.active_quests = {}
            
            return True
            
        except Exception as e:
            print(f"Error loading dialogue file: {e}")
            return False
    
    def get_current_dialogue(self) -> Optional[Dict]:
        """
        Get the current dialogue node with its text and responses.
        
        Returns:
            Dict containing dialogue information or None if invalid
        """
        if not self.current_dialogue_id or self.current_dialogue_id not in self.dialogues:
            return None
        
        return self.dialogues[self.current_dialogue_id]
    
    def choose_response(self, response_id: str) -> bool:
        """
        Process a user's response choice and update the current dialogue.
        
        Args:
            response_id: The ID of the selected response
            
        Returns:
            bool: Whether the response was valid
        """
        dialogue = self.get_current_dialogue()
        if not dialogue:
            return False
        
        # Find the response with the given ID
        for response in dialogue["responses"]:
            if response["id"] == response_id:
                # Update current dialogue
                self.current_dialogue_id = response["next_dialogue"]
                return True
        
        return False
    
    def reset_dialogue(self) -> None:
        """Reset to the starting dialogue."""
        self.current_dialogue_id = self.starting_dialogue_id


# Example usage
if __name__ == "__main__":
    # Simple test
    manager = DialogueManager()
    
    # Example dialogue file - replace with actual path
    success = manager.load_dialogue_file("dialogues/example_dialogue.json")
    
    if success:
        print("Dialogue loaded successfully!")
        
        # Get the starting dialogue
        dialogue = manager.get_current_dialogue()
        if dialogue:
            print(f"\n{dialogue['npc_name']}: {dialogue['text']}")
            
            # Display response options
            for i, response in enumerate(dialogue["responses"], 1):
                print(f"{i}. {response['text']}")
            
            # Choose the first response (for demonstration)
            if dialogue["responses"]:
                first_response = dialogue["responses"][0]
                success = manager.choose_response(first_response["id"])
                
                if success:
                    next_dialogue = manager.get_current_dialogue()
                    if next_dialogue:
                        print(f"\nNavigated to: {next_dialogue['id']}")
                        print(f"{next_dialogue['npc_name']}: {next_dialogue['text']}")
    else:
        print("Failed to load dialogue file")
