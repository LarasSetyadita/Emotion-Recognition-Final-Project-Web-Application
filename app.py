import io
import base64
from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
import tensorflow as tf

# Inisialisasi Flask app
app = Flask(__name__)

# Muat model prediksi (gantilah dengan model Anda sendiri)
model = tf.keras.models.load_model('model.h5')

# Daftar emosi yang dapat diprediksi
EMOTIONS = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Sadness', 'Surprise', 'Neutral']

# Tips penanganan untuk setiap emosi
HANDLING_TIPS = {
    'Anger': 'Cobalah untuk tetap tenang dan tarik napas.',
    'Disgust': 'Cobalah untuk menghindari pemicu ketidaksukaan.',
    'Fear': 'Cobalah untuk berbicara dengan seseorang yang Anda percayai.',
    'Happiness': 'Bagikan kebahagiaan Anda dengan orang lain.',
    'Sadness': 'Cobalah untuk berbicara dengan seseorang yang mendukung Anda.',
    'Surprise': 'Berikan waktu sejenak untuk merespons dengan tenang.',
    'Neutral': 'Tidak ada emosi yang kuat, pertimbangkan untuk mengeksplorasi perasaan Anda lebih dalam.'
}

# Fungsi untuk memproses gambar sebelum prediksi
def preprocess_image(image):
    # Ubah gambar ke format RGB dan ubah ukuran sesuai dengan model yang digunakan
    image = image.convert('RGB')
    image = image.resize((224, 224))  # Ganti ukuran sesuai kebutuhan model Anda
    image_array = np.array(image) / 255.0  # Normalisasi
    image_array = np.expand_dims(image_array, axis=0)  # Tambahkan dimensi batch
    return image_array

@app.route('/detection', methods=['POST'])
def detection():
    if request.method == 'POST':
        data = request.get_json()

        # Mengecek apakah gambar yang dikirim adalah base64 (kamera) atau file (upload)
        if data and 'image' in data:  # Jika gambar dari kamera dalam format base64
            image_data = data['image']
            img_data = base64.b64decode(image_data.split(',')[1])  # Menghapus 'data:image/png;base64,' jika ada
            img = Image.open(io.BytesIO(img_data))
        else:  # Jika gambar diunggah sebagai file
            file = request.files.get('file')
            if file:
                img = Image.open(file.stream)

        # Preprocess gambar
        processed_image = preprocess_image(img)

        # Melakukan prediksi dengan model
        predictions = model.predict(processed_image)
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        predicted_class_name = EMOTIONS[predicted_class_index]
        predicted_probability = predictions[0][predicted_class_index] * 100
        confidence = float(np.max(predictions))
        handling_tips = HANDLING_TIPS[predicted_class_name]

        # Konversi gambar ke format base64 untuk dikirim ke frontend
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        # Mengirimkan hasil prediksi dan gambar kembali ke frontend
        return jsonify({
            'emotion': predicted_class_name,
            'confidence': confidence,
            'img_base64': img_base64,
            'handling_tip': handling_tips,
            'predicted_probability': predicted_probability,
            'probabilities': {EMOTIONS[i]: predictions[0][i] * 100 for i in range(len(EMOTIONS))}
        })


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/emotion_recognition')
def emotion_recognition():
    return render_template('emotion_recognition.html')

@app.route('/article')
def article():
    return render_template('article.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        # Mendapatkan data gambar yang diproses dan hasil prediksi dari permintaan
        data = request.get_json()

        emotion = data.get('emotion')
        confidence = data.get('confidence')
        img_base64 = data.get('img_base64')
        handling_tip = data.get('handling_tip')
        predicted_probability = data.get('predicted_probability')
        probabilities = data.get('probabilities')

        return render_template('result.html',
                               emotion=emotion,
                               confidence=confidence,
                               img_base64=img_base64,
                               handling_tip=handling_tip,
                               predicted_probability=predicted_probability,
                               probabilities=probabilities)
    return render_template('result.html')



if __name__ == '__main__':
    app.run(debug=True)