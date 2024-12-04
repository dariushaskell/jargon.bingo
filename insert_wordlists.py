import json
from app import create_app
from app.models import db, JargonList, JargonItem
from flask import current_app

# Load the Flask app context
app = create_app()

def insert_word_lists(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Insert data into the database
    with app.app_context():
        categories = data.get('categories', {})

        for category_name, words in categories.items():
            # Create a new JargonList entry
            jargon_list = JargonList(
                name=category_name.capitalize(),
                description=f"{category_name.capitalize()} jargon words"
            )
            db.session.add(jargon_list)
            db.session.commit()  # Commit to get the list_id for JargonItem

            # Add words to the JargonItem table
            for word in words:
                jargon_item = JargonItem(
                    list_id=jargon_list.id,
                    term=word
                )
                db.session.add(jargon_item)

        # Commit all changes to the database
        db.session.commit()

        print("Word lists inserted successfully.")

# Path to the JSON file
json_file_path = r'C:\Users\dariu\OneDrive\Desktop\Darius\jargon-bingo\wordlists.json'  # Replace with the actual path to your JSON file

# Insert word lists into the database
insert_word_lists(json_file_path)
