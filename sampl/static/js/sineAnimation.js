const canvas = document.getElementById('sineCanvas');
const ctx = canvas.getContext('2d');

let width, height;

function resizeCanvas() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
}

let phase = 0;

function drawSine() {
    ctx.clearRect(0, 0, width, height);
    ctx.beginPath();
    ctx.strokeStyle = 'blue';
    ctx.lineWidth = 2;

    for (let x = 0; x < width; x++) {
        let y = Math.sin(x * 0.02 + phase) * 50 + height / 2;
        if (x === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }

    ctx.stroke();
    phase += 0.1;
    requestAnimationFrame(drawSine);
}

// Initial setup
resizeCanvas();
drawSine();

// Update canvas size when window is resized
window.addEventListener('resize', () => {
    resizeCanvas();
});
