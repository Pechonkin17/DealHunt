
const slider = document.getElementById("priceRange");
slider.addEventListener("input", function () {
    const value = (this.value - this.min) / (this.max - this.min) * 100;
    this.style.background = `linear-gradient(to right, #4D1223 0%, #4D1223 ${value}%, #2c2c2c ${value}%, #2c2c2c 100%)`;
});

// Ініціалізуємо при завантаженні
slider.dispatchEvent(new Event("input"));

