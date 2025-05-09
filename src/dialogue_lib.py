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

    def load_dialogue_from_string(self, json_string: str) -> bool:
        """
        Load dialogue data directly from a JSON string.
        Useful for web interfaces with file upload.
        
        Args:
            json_string: JSON string containing dialogue data
            
        Returns:
            bool: True if loading succeeded, False otherwise
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
            else:
                self.quests = {}
                
            self.active_quests = {}
            
            return True
            
        except Exception as e:
            print(f"Error parsing dialogue JSON: {e}")
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
        
        return errors


# Simple usage example
if __name__ == "__main__":
    # Test the library functionality
    manager = DialogueManager()
    success = manager.load_dialogue_file("../json/example-dialogue-json.json")
    
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