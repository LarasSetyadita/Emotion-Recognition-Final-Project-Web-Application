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
    image = image.resize((224, 224))  # Ganti ukuran sesuai kebutuhan model Anda
    image_array = np.array(image) / 255.0  # Normalisasi
    image_array = np.expand_dims(image_array, axis=0)  # Tambahkan dimensi batch
    return image_array


@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        # Periksa apakah file diunggah
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template(error="No file selected")

        try:
            # Proses gambar langsung dari request.files tanpa menyimpannya ke disk
            image = Image.open(file.stream)  # Membaca gambar dari stream (memori)
            processed_image = preprocess_image(image)

            # Prediksi
            predictions = model.predict(processed_image)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_probability = predictions[0][predicted_class_index] * 100  # Akurasi untuk kelas prediksi terpilih
            predicted_class_name = EMOTIONS[predicted_class_index]
            handling_tips = HANDLING_TIPS[predicted_class_name]
            confidence = float(np.max(predictions))

            # Konversi gambar ke format base64 agar bisa ditampilkan di web
            img_io = io.BytesIO()
            image.save(img_io, 'PNG')  # Menyimpan gambar dalam format PNG
            img_io.seek(0)
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

            # Render hasil di halaman yang sama
            return render_template(
                'emotion_recognition.html',
                predicted_class=predicted_class_name,
                handling_tip=handling_tips,
                confidence_score=confidence,
                file_uploaded=True,
                img_base64=img_base64,  # Gambar dalam base64 untuk ditampilkan
                predicted_probability=predicted_probability,
                probabilities={EMOTIONS[i]: predictions[0][i] * 100 for i in range(len(EMOTIONS))}
            )
        except Exception as e:
            return render_template('base.html', error=f"Error processing image: {str(e)}")

    # Jika GET request, tampilkan formulir upload
    return render_template('emotion_recognition.html')


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