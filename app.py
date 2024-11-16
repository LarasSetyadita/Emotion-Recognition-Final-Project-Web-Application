from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/emotion_recognition')
def emotion_recognition():
    return render_template('emotion_recognition.html')

@app.route('/article')
def article():
    return render_template('article.html')

if __name__ == "__main__":
    app.run(debug=True)