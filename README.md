A simple and effective tool for managing assignments between teachers and students. Built using **FastAPI** on the backend and a lightweight frontend with **HTML, CSS, and JavaScript** (or React if you prefer). It includes role-based login, assignment creation, submissions, and a clean API.
1. Clone the Project
git clone (https://github.com/Druthi93/EDTECH-ASSIGNMENT/).git
cd edtech-assignment-tracker
2. Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
3. Install Requirements
pip install -r requirements.txt
4. Run the Server
uvicorn main:app --reload
5. Test It Out
Open your browser and go to:
http://localhost:8000/docs
