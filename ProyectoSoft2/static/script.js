document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger-menu');
    const navbar = document.querySelector('.navbar');

    hamburger.addEventListener('click', () => {
        navbar.classList.toggle('active');
    });

    // Funcionalidad del carrusel
    let currentSlide = 0; // Índice de la diapositiva actual
    const slides = document.querySelectorAll('.carousel-item'); // Todas las diapositivas del carrusel

    // Muestra la diapositiva en el índice especificado
    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.style.transform = `translateX(${100 * (i - index)}%)`; // Ajusta la posición de cada diapositiva
        });
    }

    // Mueve a la siguiente diapositiva
    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length; // Cicla al principio si está en la última diapositiva
        showSlide(currentSlide);
    }

    // Mueve a la diapositiva anterior
    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length; // Cicla al final si está en la primera diapositiva
        showSlide(currentSlide);
    }

    // Asigna eventos de clic a los botones de control del carrusel
    document.querySelector('.carousel-control-next').addEventListener('click', nextSlide);
    document.querySelector('.carousel-control-prev').addEventListener('click', prevSlide);

    // Inicializa el carrusel mostrando la primera diapositiva
    showSlide(currentSlide);

    // Opcional: Cambio automático de diapositivas cada 5 segundos
    setInterval(nextSlide, 5000);


    document.addEventListener('DOMContentLoaded', function () {
    const features = document.querySelectorAll('.feature');

    features.forEach(feature => {
        feature.addEventListener('mouseenter', () => {
            feature.style.transform = 'translateY(-10px)';
        });

        feature.addEventListener('mouseleave', () => {
            feature.style.transform = 'translateY(0)';
        });
    });
    });
    document.getElementById('search-button').addEventListener('click', function() {
        var popover = document.getElementById('search-filters');
        if (popover.style.display === 'none' || popover.style.display === '') {
            popover.style.display = 'block';
        } else {
            popover.style.display = 'none';
        }
    });
});
