# Emotion-Recognition-Final-Project-Web-Application
This repository stores the final assignment code for the 5th semester web application subject.

# Description
This project develops machine learning to analyze human emotions through images.

## Installation
1. Clone the repository:
<br><code>git clone https://github.com/LarasSetyadita/streamlit-emotions-classification.git</code></br>
2. Install the required packages:
<br><code>pip install -r requirements.txt</code></br>
2. Install tailwind CLI:
<br><code>npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --watch
</code></br>

## Usage
1. Run the Streamlit application:
<br><code>python app.py</code></br>

## Emotion Analysis
The dashboard can identify several emotions from images:
- <b>Happy:</b> Recognizes joy and positive expressions. Suggestions include celebrating small moments and sharing happiness.
- <b>Sad:</b> Detects sadness or melancholy. Suggestions include allowing yourself to feel and seeking support.

- <b>Angry:</b> Identify frustration or anger. Suggestions include calming techniques and communicating feelings.
- <b>Neutral:</b> Recognize a state of balance. Encourage reflection or trying new activities.
- <b>Surprised:</b> Capture unexpected reactions. Encourage reflection and journaling.
- <b>Emotion not found:</b> occurs when the emotion index found is less than 80%
