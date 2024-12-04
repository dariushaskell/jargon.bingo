import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
print(f"Loading .env file from: {dotenv_path}")
load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)), debug=True)
