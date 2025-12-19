import streamlit as st

st.set_page_config(layout="wide")

html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
    margin: 0;
    background: #1b5e20;
}
canvas {
    display: block;
    margin: auto;
    background: linear-gradient(#4caf50, #2e7d32);
    touch-action: none;
}
</style>
</head>
<body>

<canvas id="game" width="900" height="500"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let level = 1;
let strokes = 0;

let ball = { x: 120, y: 250, vx: 0, vy: 0, r: 10 };
let hole = { x: 760, y: 250, r: 16 };

let obstacles = [];

let dragging = false;
let dragStart = {};
let dragEnd = {};

function buildLevel() {
    obstacles = [];

    if (level === 1) {
        obstacles.push({x: 420, y: 120, w: 30, h: 260});
    }
    if (level === 2) {
        obstacles.push({x: 300, y: 80, w: 30, h: 340});
        obstacles.push({x: 560, y: 80, w: 30, h: 340});
    }
    if (level >= 3) {
        obstacles.push({x: 250, y: 220, w: 220, h: 30});
        obstacles.push({x: 520, y: 60, w: 30, h: 300});
        obstacles.push({x: 650, y: 200, w: 30, h: 200});
    }
}

function resetLevel() {
    ball.x = 120;
    ball.y = 250;
    ball.vx = 0;
    ball.vy = 0;
    strokes = 0;

    hole.x = 720 + (level * 10);
    hole.y = 120 + (level * 70) % 260;

    buildLevel();
}

canvas.addEventListener("pointerdown", e => {
    dragging = true;
    dragStart = { x: e.offsetX, y: e.offsetY };
});

canvas.addEventListener("pointermove", e => {
    if (dragging) {
        dragEnd = { x: e.offsetX, y: e.offsetY };
    }
});

canvas.addEventListener("pointerup", e => {
    dragging = false;
    let dx = dragStart.x - dragEnd.x;
    let dy = dragStart.y - dragEnd.y;
    ball.vx = dx * 0.18;
    ball.vy = dy * 0.18;
    strokes++;
});

function collideRect(rect) {
    let closestX = Math.max(rect.x, Math.min(ball.x, rect.x + rect.w));
    let closestY = Math.max(rect.y, Math.min(ball.y, rect.y + rect.h));

    let dx = ball.x - closestX;
    let dy = ball.y - closestY;

    if (dx*dx + dy*dy < ball.r*ball.r) {
        if (Math.abs(dx) > Math.abs(dy)) {
            ball.vx *= -1;
        } else {
            ball.vy *= -1;
        }
    }
}

function update() {
    ball.x += ball.vx;
    ball.y += ball.vy;

    ball.vx *= 0.985;
    ball.vy *= 0.985;

    if (ball.x < ball.r || ball.x > canvas.width - ball.r) ball.vx *= -1;
    if (ball.y < ball.r || ball.y > canvas.height - ball.r) ball.vy *= -1;

    obstacles.forEach(collideRect);

    let dx = ball.x - hole.x;
    let dy = ball.y - hole.y;
    if (Math.sqrt(dx*dx + dy*dy) < hole.r) {
        level++;
        resetLevel();
    }
}

function drawArrow() {
    if (!dragging) return;
    ctx.strokeStyle = "white";
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(ball.x, ball.y);
    ctx.lineTo(dragEnd.x, dragEnd.y);
    ctx.stroke();
}

function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);

    // Obstacles
    ctx.fillStyle = "#3e2723";
    obstacles.forEach(o => ctx.fillRect(o.x, o.y, o.w, o.h));

    // Hole
    ctx.beginPath();
    ctx.arc(hole.x, hole.y, hole.r, 0, Math.PI*2);
    ctx.fillStyle = "black";
    ctx.fill();

    // Ball
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2);
    ctx.fillStyle = "white";
    ctx.fill();

    drawArrow();

    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.fillText("Level: " + level, 20, 30);
    ctx.fillText("Strokes: " + strokes, 20, 60);
}

function loop() {
    update();
    draw();
    requestAnimationFrame(loop);
}

resetLevel();
loop();
</script>

</body>
</html>
"""

st.components.v1.html(html, height=520)
