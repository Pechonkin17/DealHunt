const centerY = window.innerHeight / 2;

function updateBlur() {
    document.querySelectorAll('.game-card').forEach(card => {
        const rect = card.getBoundingClientRect();
        const cardY = rect.top + rect.height / 2;
        const distance = Math.abs(centerY - cardY);

        const maxDistance = window.innerHeight / 2;
        const blurAmount = 12 - Math.min((distance / maxDistance) * 12, 12);

        card.style.backdropFilter = `blur(${blurAmount}px)`;
    });
}

window.addEventListener('scroll', updateBlur);
window.addEventListener('resize', updateBlur);
window.addEventListener('load', updateBlur);