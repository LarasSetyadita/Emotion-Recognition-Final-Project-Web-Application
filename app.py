import io
import base64

import cv2
from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
import tensorflow as tf

# Inisialisasi Flask app
app = Flask(__name__)

# Muat model prediksi
model = tf.keras.models.load_model('model.h5')

# Daftar emosi yang dapat diprediksi
EMOTIONS = ['Anger', 'Happiness', 'Sadness', 'Surprise', 'Neutral']

# Tips penanganan untuk setiap emosi
HANDLING_TIPS = {
    'Anger': 'When feeling angry, it’s essential to pause and allow yourself to experience the emotion without acting on it immediately. Research suggests that using calming techniques, such as deep breathing, mindfulness, or progressive muscle relaxation, can help reduce the intensity of anger. It’s also important to identify the underlying causes of your anger—whether it’s frustration, hurt, or feeling misunderstood. Talking to someone you trust can help you process your feelings. Lastly, channeling your anger into constructive activities, like exercise or creative outlets, can help release the built-up tension in a healthy way.',
    'Happiness': '"Great to see youre feeling happy! Research suggests that maintaining a positive mindset can boost both your mental and physical well-being. To enhance this feeling, consider sharing your joy with others through social connections or engaging in activities that bring you further happiness. Studies show that helping others or expressing gratitude can elevate positive emotions even more. Keep spreading that positive energy!',
    'Sadness': 'When feeling sad, it can be helpful to allow yourself to express your emotions rather than suppress them. Engaging in activities that you find comforting, such as listening to soothing music or journaling, can provide relief. It’s also beneficial to reach out to a trusted friend or professional who can offer support. Studies have shown that social connection and self-compassion are key factors in improving emotional resilience during tough times.',
    'Surprise': 'When experiencing surprise, it’s important to first take a moment to process the situation. Allowing yourself to pause and reflect can help you manage your immediate reaction, especially if the surprise is unexpected or overwhelming. Engaging in deep breathing or grounding exercises can help regain balance. Research suggests that pausing before reacting gives you time to evaluate how to respond thoughtfully. It’s also helpful to talk through the experience with others to gain perspective and understand your emotional response better.',
    'Neutral': 'When feeling angry, it’s important to recognize and acknowledge the emotion before reacting. Research shows that taking a few deep breaths or counting to ten can help calm the mind and body, preventing impulsive reactions. It can also be helpful to step away from the situation momentarily to give yourself space. Engaging in physical activity, such as going for a walk or exercising, can help release the built-up tension. Additionally, expressing your feelings calmly and assertively to the person involved can lead to better understanding and resolution..'
}

# Fungsi untuk memproses gambar sebelum prediksi
def preprocess_image(image):
    image = image.convert('RGB')  # Konversi ke RGB jika belum
    image = image.resize((150, 150))  # Ganti ukuran sesuai kebutuhan model Anda
    image_array = np.array(image) / 255.0  # Normalisasi
    image_array = np.expand_dims(image_array, axis=0)  # Tambahkan dimensi batch
    return image_array

@app.route('/detection', methods=['GET', 'POST'])
def detection():
    if request.method == 'POST':
        # Periksa apakah file diunggah
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template('emotion_recognition.html', error="No file selected")

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
            confidence = float(np.max(predictions)) * 100

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
            return render_template('emotion_recognition.html', error=f"Error processing image: {str(e)}")

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


if __name__ == '__main__':
    app.run(debug=True)
