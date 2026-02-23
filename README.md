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
│   ...
├── components/                     # Reusable UI components
├── utils/                          # Python package with helper functions and data models
│   ├── models.py                   # Pydantic models (Question, QuestionCollection)
│   ├── loader.py                   # JSON loading utilities
│   ...
├── data/                           # Assessment data and configurations                      # Data configuration files in JSON or Markdown content for the site go here
│   ├── questions.json
│   ...
├── .devcontainer/                  # Automatically added by [Streamlit Community Cloud for GitHub Codespaces](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/edit-your-app)
└── requirements.txt                # Python dependencies
```

## Question Configuration

All questions are configured in the JSON file in the `data/questions.json` directory, which can be considered our full question database. The JSON follows this structure, with each question represented as a JSON object with a unique "question_id":

```json
{
  "questions": [
    {
      "question_id": "unique_id",
      "question_text": "Your question here?",
      "question_type": "categorical",
      "answer_options": [
        ["Option 1", -1.0],
        ["Option 2", 2.0]
      ],
      "importance_score": 1.0
    }
  ]
}
```

The question fields indicate:
- `question_type`: Can be "categorical" (default) for text responses or "range" for a range of numberical values.
- `answer_options`: List of [text, score] tuples. Answers that result in an easier path to completing the project should be given a positive score greater than 0, with magnitude expressing how much easier. Answers that make a project more challenging should have a negative score less than 0, with lower numbers (larger magnitude or absolute value) reflecting larger challenges. For answers that are neutral, set their score to 0.
- `importance_score`: Weight of the question in overall scoring (default: 1.0). Make this larger if you feel a question is more important than others in the same scoring categories.

## Displaying Questions
Grouping questions to be displayed on a particular page is done by simply listing question ids in a JSON file as follows:
```json
{
  "question_ids": [
    "T-0001",
    "T-0002",
    "T-0003",
    "T-0004",
    "T-0005",
    ...
}
```
Set up your application pages in the `pages` folder to read from the appropriate JSON file.

## Scoring Rubric Configuration
Scoring configurations with thresholds to determine the final decision to display are defined separately from questions and display pages, so that you can score on more parameters than there are pages and use the same questions in multiple scoring rubrics.

The normalized scoring ranges for each rubric range from -1 to 1, so ensure threshold values are within this range. This allows you to use the same thresholds even if the importance of questions is changed. A script to validate the scoring rubric and compute minimum and maximum scores is available in `utils/analyze_scoring.py` and can be run with `python -m utils.analyze_scoring --help`.

Define your scoring rubric with a display header, list of question ids, and thresholds with a header, description, color, upper bound (exlusive) and lower (inclusive) bound range. If the upper bound is left out, it's assumed to be infinity, and if the lower bound is left out, it's assumed to be negative infinity. One of the thresholds will be displayed on the final results page for each scoring rubric, depending on what the responses to questions are.

Here is an example of the threshold configuration file. Note that the upper and lower bound are adjacent intervals and with endpoints ranging between -1 and 1:
```json
{
    "header": "Rubric Name Display Header ",
    "question_ids": ["O-0001", "O-0004", "T-0005", "T-0006", "T-0011"],
    "thresholds": [
        {"upper": -0.5, "header": "Low scoring result", "description": "This will be challenging", "color": "violet"},
        {"lower": -0.5, "upper":0.5, "header": "Medium scoring result", "description": "This will be moderately challenging, but achievable", "color": "blue"},
        {"lower":0.5, "header": "Easy result", "description": "This shouldn't be too hard", "color":"green"}
    ]
}
```

## Development

Format and lint code with ruff:
```bash
ruff check .
ruff format .
```

# Contributions
This tool was collaboratively developed at the [2026 Dagstuhl AI for Social Good Seminar](https://www.dagstuhl.de/26021). If you have feedback, please contact us by filling out our [Google Form](https://forms.gle/erA7MhvmoNG6sy668) or submitting an issue on [GitHub](https://github.com/ginic/AI4SG_UseCaseAssessment).