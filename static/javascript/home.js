let currentIndex = 0;
const slidesContainer = document.querySelector('.slides-container');
const slides = document.querySelectorAll('.slide');

function showSlide(index) {
    slidesContainer.style.transform = `translateX(-${index * 100}%)`;
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
}

function prevSlide() {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(currentIndex);
}

document.getElementById('nextSlide').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % slides.length;
    showSlide(currentIndex);
});

document.getElementById('prevSlide').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length;
    showSlide(currentIndex);
});

setInterval(nextSlide, 5000);
showSlide(currentIndex);