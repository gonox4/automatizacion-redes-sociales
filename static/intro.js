console.log("Intro loaded");

const introLayer = document.getElementById('intro-layer');
const appLayer = document.getElementById('app-layer');
const rocketContainer = document.getElementById('rocket-container');
const mouseHint = document.getElementById('click-hint');

// --- Starfield (Simplified) ---
const starCanvas = document.getElementById('starfield');
const sCtx = starCanvas.getContext('2d');
let stars = [];
let w = (starCanvas.width = window.innerWidth);
let h = (starCanvas.height = window.innerHeight);

for (let i = 0; i < 150; i++) {
    stars.push({ x: Math.random() * w, y: Math.random() * h, s: Math.random() * 2 });
}

function draw() {
    sCtx.fillStyle = '#000';
    sCtx.fillRect(0, 0, w, h);
    sCtx.fillStyle = '#fff';
    stars.forEach(s => {
        sCtx.beginPath();
        sCtx.arc(s.x, s.y, s.s, 0, Math.PI * 2);
        sCtx.fill();
        s.y += s.s * 3;
        if (s.y > h) s.y = 0;
    });
    requestAnimationFrame(draw);
}
draw();

// --- Sequence ---
let started = false;

function startSequence() {
    if (started) return;
    started = true;
    console.log("Animation sequence starting");

    if (mouseHint) mouseHint.innerText = "LAUNCHING...";

    // Rocket animation
    if (rocketContainer) {
        rocketContainer.style.transform = "translateY(-1500px) scale(0)";
        rocketContainer.style.opacity = "0";
    }

    // Actual transition
    setTimeout(() => {
        // Show App
        if (appLayer) {
            appLayer.classList.remove('hidden');
            void appLayer.offsetWidth;
            appLayer.classList.add('visible');
        }

        // Hide Intro Layer
        if (introLayer) {
            introLayer.style.opacity = "0";
            setTimeout(() => {
                introLayer.style.display = "none";
            }, 800);
        }
    }, 1200);
}

// Global click listeners
document.body.addEventListener('click', startSequence);
if (mouseHint) mouseHint.addEventListener('click', startSequence);

// Failsafe: start after 5 seconds automatically
setTimeout(() => {
    if (!started) {
        console.log("Failsafe: Auto-starting");
        startSequence();
    }
}, 5000);
