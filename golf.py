// Inside your <script> for the golf game

let dragStart = null;

// Draw function update: draw arrow if dragging
function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    // Green background
    ctx.fillStyle = "#3cba54";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    // Obstacles
    for(let obs of obstacles){
        ctx.fillStyle = obs.type==='sand'?'#f4d27c':'#4fc3f7';
        ctx.fillRect(obs.x, obs.y, obs.w, obs.h);
    }

    // Hole
    ctx.fillStyle = "black";
    ctx.beginPath();
    ctx.arc(hole.x, hole.y, hole.radius, 0, 2*Math.PI);
    ctx.fill();

    // Ball
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, 2*Math.PI);
    ctx.fill();

    // Draw arrow if dragging
    if(dragStart && !moving){
        ctx.strokeStyle = "red";
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(ball.x, ball.y);
        ctx.lineTo(dragStart.x, dragStart.y);
        ctx.stroke();
        // Optional arrowhead
        let dx = dragStart.x - ball.x;
        let dy = dragStart.y - ball.y;
        let angle = Math.atan2(dy, dx);
        let headLength = 15;
        ctx.beginPath();
        ctx.moveTo(dragStart.x, dragStart.y);
        ctx.lineTo(dragStart.x - headLength * Math.cos(angle - Math.PI/6), 
                   dragStart.y - headLength * Math.sin(angle - Math.PI/6));
        ctx.lineTo(dragStart.x - headLength * Math.cos(angle + Math.PI/6), 
                   dragStart.y - headLength * Math.sin(angle + Math.PI/6));
        ctx.lineTo(dragStart.x, dragStart.y);
        ctx.fillStyle = "red";
        ctx.fill();
    }
}

// Pointer events for drag
canvas.addEventListener("pointerdown", (e)=>{
    if(!moving){
        dragStart = {x:e.offsetX, y:e.offsetY};
    }
});

canvas.addEventListener("pointermove", (e)=>{
    if(dragStart && !moving){
        dragStart = {x:e.offsetX, y:e.offsetY};
    }
});

canvas.addEventListener("pointerup", (e)=>{
    if(dragStart && !moving){
        let dx = dragStart.x - e.offsetX;
        let dy = dragStart.y - e.offsetY;
        velocity.x = dx/5;
        velocity.y = dy/5;
        moving = true;
        shots += 1;
        dragStart = null;
    }
});
