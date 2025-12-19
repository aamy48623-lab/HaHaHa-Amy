import streamlit as st

st.set_page_config(layout="wide")

html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1.0, user-scalable=no">
<style>
html, body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: #1b5e20;
}
canvas {
    display: block;
    background: linear-gradient(#4caf50, #2e7d32);
    touch-action: none;
}
</style>
</head>
<body>

<canvas id="game"></canvas>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

let level = 1;
let strokes = 0;

let ball = { x: 80, y: 200, vx: 0, vy: 0, r: 10 };
let hole = { x: 0, y: 0, r: 18 };

let obstacles = [];

let dragging = false;
let dragStart = {x:0,y:0};
let dragEnd = {x:0,y:0};

function buildLevel() {
    obstacles = [];
    const w = canvas.width;
    const h = canvas.height;

    if (level === 1) {
        obstacles.push({x: w*0.5, y: h*0.2, w: 30, h: h*0.6});
    }
    if (level === 2) {
        obstacles.push({x: w*0.35, y: h*0.1, w: 30, h: h*0.8});
        obstacles.push({x: w*0.65, y: h*0.1, w: 30, h: h*0.8});
    }
    if (level >= 3) {
        obstacles.push({x: w*0.25, y: h*0.5, w: w*0.35, h: 30});
        obstacles.push({x: w*0.6, y: h*0.15, w: 30, h: h*0.5});
    }
}

function resetLevel() {
    ball.x = 80;
    ball.y = canvas.height / 2;
    ball.vx = 0;
    ball.vy = 0;
    strokes = 0;

    hole.x = canvas.width - 80;
    hole.y = canvas.height * (0.3 + (level % 3) * 0.2);

    buildLevel();
}

function getPos(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
}

canvas.addEventListener("pointerdown", e => {
    dragging = true;
    dragStart = getPos(e);
    dragEnd = dragStart;
});

canvas.addEventListener("pointermove", e => {
    if (!dragging) return;
    dragEnd = getPos(e);
});

canvas.addEventListener("pointerup", e => {
    dragging = false;
    let dx = dragStart.x - dragEnd.x;
    let dy = dragStart.y - dragEnd.y;
    ball.vx = dx * 0.18;
    ball.vy = dy * 0.18;
    strokes++;
});

function collideRect(o) {
    let cx = Math.max(o.x, Math.min(ball.x, o.x + o.w));
    let cy = Math.max(o.y, Math.min(ball.y, o.y + o.h));
    let dx = ball.x - cx;
    let dy = ball.y - cy;

    if (dx*dx + dy*dy < ball.r*ball.r) {
        if (Math.abs(dx) > Math.abs(dy)) ball.vx *= -1;
        else ball.vy *= -1;
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

    ctx.fillStyle = "#3e2723";
    obstacles.forEach(o => ctx.fillRect(o.x, o.y, o.w, o.h));

    ctx.beginPath();
    ctx.arc(hole.x, hole.y, hole.r, 0, Math.PI*2);
    ctx.fillStyle = "black";
    ctx.fill();

    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2);
    ctx.fillStyle = "white";
    ctx.fill();

    drawArrow();

    ctx.fillStyle = "white";
    ctx.font = "18px Arial";
    ctx.fillText("Level " + level, 16, 28);
    ctx.fillText("Strokes " + strokes, 16, 52);
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

st.components.v1.html(html, height=800)
