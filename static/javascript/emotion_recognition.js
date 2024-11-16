const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const capturedImage = document.getElementById('capturedImage');
const captured = document.getElementById('captured');
const fileInput = document.getElementById('fileInput');
const inputSource = document.getElementById('inputSource');
const file = document.getElementById('file');

// Fungsi untuk meminta akses kamera
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        console.error("Error accessing camera: ", error);
    }
}

// Fungsi untuk menangkap gambar dari kamera
captureButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    const size = Math.min(video.videoWidth, video.videoHeight); // Dimensi persegi berdasarkan ukuran terkecil
    canvas.width = size;
    canvas.height = size;
    context.drawImage(
        video,
        (video.videoWidth - size) / 2, // Crop horizontal dari tengah
        (video.videoHeight - size) / 2, // Crop vertikal dari tengah
        size,
        size,
        0,
        0,
        size,
        size
    );

    const imageUrl = canvas.toDataURL('image/png');
    capturedImage.src = imageUrl;
    captured.classList.remove('hidden');
});

// Fungsi untuk mengganti input antara kamera dan file
inputSource.addEventListener('change', () => {
    if (inputSource.value === 'Camera') {
        fileInput.classList.add('hidden');
        document.getElementById('cameraInput').classList.remove('hidden');
        startCamera();
    } else if (inputSource.value === 'File') {
        fileInput.classList.remove('hidden');
        document.getElementById('cameraInput').classList.add('hidden');
        const stream = video.srcObject;
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
        }
        video.srcObject = null;
    }
});

// Fungsi untuk menampilkan gambar hasil upload file
file.addEventListener('change', () => {
    const fileReader = new FileReader();
    fileReader.onload = function (e) {
        capturedImage.src = e.target.result;
        captured.classList.remove('hidden');
    };
    fileReader.readAsDataURL(file.files[0]);
});

// Memulai kamera saat halaman dimuat
window.addEventListener('load', startCamera);
