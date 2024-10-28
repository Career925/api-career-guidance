import json
import os
from datetime import datetime
import pytz

class DatabaseHandler:
    def __init__(self, file_path="data.json", timezone="Asia/Kolkata"):
        self.file_path = file_path
        self.timezone = timezone
        # Ensure file exists and is initialized as an empty list if it doesn't
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)  # Initialize with an empty list
    
    def _load_data(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)
            # Ensure data is a list, convert if necessary
            if isinstance(data, dict):
                data = []  # Reset to an empty list if it's a dictionary
        return data
    
    def _save_data(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
    
    def _get_formatted_datetime(self):
        current_time = datetime.now(pytz.timezone(self.timezone))
        # Get the formatted datetime string without the colon in the offset
        formatted_datetime = current_time.strftime("%d %B %Y %I:%M %p %z")
        # Insert the colon in the timezone offset manually
        return formatted_datetime[:-2] + ":" + formatted_datetime[-2:]
    
    def add_question(self, question, answer):
        data = self._load_data()
        lower_question = question.lower()
        
        # Check if question already exists in lowercase
        for entry in data:
            if entry["ques"].lower() == lower_question:
                print("This question already exists.")
                return  # Exit the function without adding the duplicate
        
        # Add the new question-answer entry if it's not a duplicate
        new_entry = {
            "ques": lower_question,  # Save question in lowercase
            "ans": answer,
            "dateTime": self._get_formatted_datetime()
        }
        data.append(new_entry)
        self._save_data(data)
        print("Question added successfully.")
    
    def remove_question(self, question):
        data = self._load_data()
        lower_question = question.lower()
        data = [entry for entry in data if entry["ques"].lower() != lower_question]
        self._save_data(data)
        print("Question removed successfully if it existed.")
    
    def edit_question(self, question, new_answer):
        data = self._load_data()
        lower_question = question.lower()
        
        for entry in data:
            if entry["ques"].lower() == lower_question:
                entry["ans"] = new_answer
                entry["dateTime"] = self._get_formatted_datetime()
                self._save_data(data)
                print("Question updated successfully.")
                return
        print("Question not found.")
    
    def get_answer(self, question):
        data = self._load_data()
        lower_question = question.lower()
        
        for entry in data:
            if entry["ques"].lower() == lower_question:
                return entry["ans"]
        return "Question not found."
    
    def list_all_questions(self):
        data = self._load_data()
        return [entry["ques"] for entry in data]

