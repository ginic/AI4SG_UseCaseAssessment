# AI4SG Use Case Assessment

Interactive assessment framework for scoping AI, machine learning and data science projects for social good organizations.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- Pydantic (data validation and modeling)
- Ruff (linting and formatting to keep the code readable)

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Project Structure

```
.
├── app.py                          # Main application entry point
├── pages/                          # Multi-page app pages
│   ├── 1_Organizational_Constraints.py
│   ├── 2_Technical_Constraints.py
│   └── 3_Results.py
├── components/                     # Reusable UI components
├── utils/                          # Helper functions and utilities
│   ├── models.py                   # Pydantic models (Question, QuestionCollection)
│   ├── loader.py                   # JSON loading utilities
│   └── config.py                   # Configuration and paths
├── data/                           # Assessment data and configurations
│   ├── organizational_questions.json
│   └── technical_questions.json
└── requirements.txt                # Python dependencies
```

## Question Configuration

Questions are configured using JSON files in the `data/` directory. Each question follows this structure:

```json
{
  "questions": [
    {
      "question_id": "unique_id",
      "question_text": "Your question here?",
      "question_type": "categorical",
      "answer_options": [
        ["Option 1", 1.0],
        ["Option 2", 2.0]
      ],
      "importance_score": 1.0
    }
  ]
}
```

- `question_type`: Can be "categorical" (default) or "range"
- `answer_options`: List of [text, score] tuples
- `importance_score`: Weight of the question in overall scoring (default: 1.0)

## Development

Format and lint code with ruff:
```bash
ruff check .
ruff format .
```
