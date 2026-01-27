# Good Tech Reality Check
A web interface to the interactive assessment framework for scoping AI, machine learning and data science projects for social good organizations.

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
streamlit run Introduction.py
```

The application will open in your default web browser at `http://localhost:8501`.


## Deployment
This application can be deployed on [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud).


## Project Structure

```
.
├── Introduction.py                          # Main application entry point
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
├── .devcontainer/                  # Automatically added by [Streamlit Community Cloud for GitHub Codespaces](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/edit-your-app)
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

# Contributions
This tool was collaboratively developed at the [2026 Dagstuhl AI for Social Good Seminar](https://www.dagstuhl.de/26021). If you have feedback, please contact us by filling out our [Google Form](https://forms.gle/erA7MhvmoNG6sy668) or submitting an issue on [GitHub](https://github.com/ginic/AI4SG_UseCaseAssessment).