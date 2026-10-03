# SmartMovie AI — Recommendation System

**Student:** Avinash  
**Course:** MSAI 631 – Artificial Intelligence for Human-Computer Interaction

SmartMovie AI is a content-based movie recommender created for the AI/HCI project. It converts movie genres and keywords into TF-IDF vectors, compares them with cosine similarity, and presents ranked recommendations in a Tkinter GUI.

## Features
- Content-based AI recommendation
- TF-IDF vectorization and cosine similarity
- Desktop GUI
- Movie selector and genre filter
- Adjustable result count
- Similarity percentages
- Explanation of shared genres
- Validation and unit tests

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

On Windows activate with `.venv\Scripts\activate`.

## Test
```bash
python -m unittest test_recommender.py -v
```

## Project structure
```text
app.py
recommender.py
test_recommender.py
requirements.txt
README.md
FOUNDATION_AND_CREDITS.md
GITHUB_UPLOAD.md
data/movies.csv
screenshots/README.txt
```

## Dataset
The bundled dataset uses fictional movie titles and project-created keywords, so the project does not reproduce copyrighted movie summaries.

## HCI extensions
The GUI adds a selectable title list, genre filtering, adjustable result count, similarity feedback, explanations, error handling, and status feedback. These changes make a basic similarity algorithm easier to understand and control.

## GitHub
Create a repository named `avinash-ai-hci-recommendation-system`, push these files, and paste the real repository URL into the report. If private, grant the instructor access.
