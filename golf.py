import streamlit as st

st.set_page_config(layout="wide")

html = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    background: #2e7d32;
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

let dragging = false;
let dragStart = {};
let dragEnd = {};

function resetLevel() {
    ball.x = 120;
    ball.y = 250;
    ball.vx = 0;
    ball.vy = 0;
    strokes = 0;

    hole.x = 700 + level * 20;
    hole.y = 150 + level * 40;
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

function update() {
    ball.x += ball.vx;
    ball.y += ball.vy;

    ball.vx *= 0.985;
    ball.vy *= 0.985;

    if (ball.x < ball.r || ball.x > canvas.width - ball.r) ball.vx *= -1;
    if (ball.y < ball.r || ball.y > canvas.height - ball.r) ball.vy *= -1;

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
