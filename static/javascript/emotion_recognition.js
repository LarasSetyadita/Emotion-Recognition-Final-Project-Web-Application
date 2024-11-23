const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const capturedImage = document.getElementById('capturedImage');
const captured = document.getElementById('captured');
const fileInput = document.getElementById('fileInput');
const cameraInput = document.getElementById('cameraInput');
const fileUpload = document.getElementById('filei');
const cameraBtn = document.getElementById('CameraBtn');
const fileBtn = document.getElementById('FileBtn');

// Fungsi untuk memulai kamera
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        console.error("Error accessing camera: ", error);
    }
}

// Fungsi untuk menghentikan kamera
function stopCamera() {
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
    }
}

// Tombol Kamera
cameraBtn.addEventListener('click', () => {
    fileInput.classList.add('hidden');
    cameraInput.classList.remove('hidden');
    captured.classList.add('hidden');
    startCamera();
});

// Tombol File
fileBtn.addEventListener('click', () => {
    stopCamera();
    cameraInput.classList.add('hidden');
    fileInput.classList.remove('hidden');
    captured.classList.add('hidden');
});

// Capture Gambar
captureButton.addEventListener('click', async () => {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageUrl = canvas.toDataURL('image/png');
    capturedImage.src = imageUrl;
    captured.classList.remove('hidden');

    // Kirim gambar ke server untuk analisis
    const response = await fetch('/detection', {
        method: 'POST',
        body: JSON.stringify({ image: imageUrl }),
        headers: {
            'Content-Type': 'application/json',
        },
    });

    const result = await response.json();
    displayResult(result);
});

// Menampilkan hasil analisis
function displayResult(result) {
    const resultDiv = document.getElementById('result');
    if (result.error) {
        resultDiv.innerHTML = `<p>${result.error}</p>`;
    } else {
        resultDiv.innerHTML = `
            <p><strong>Emotion:</strong> ${result.emotion}</p>
            <p><strong>Confidence:</strong> ${result.confidence}%</p>
        `;
    }
}


// Upload File
fileUpload.addEventListener('change', () => {
    const reader = new FileReader();
    reader.onload = (e) => {
        capturedImage.src = e.target.result;
        captured.classList.remove('hidden');
    };
    reader.readAsDataURL(fileUpload.files[0]);
});

// Memulai kamera saat halaman dimuat
window.addEventListener('load', startCamera);