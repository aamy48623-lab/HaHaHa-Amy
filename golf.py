import streamlit as st

st.set_page_config(layout="wide")
st.title("⛳ 高階高爾夫遊戲")

html_code = """
<canvas id="golfCanvas" width="800" height="600" style="border:1px solid #000000; touch-action: none;"></canvas>
<p id="score"></p>
<p id="level"></p>

<script>
const canvas = document.getElementById("golfCanvas");
const ctx = canvas.getContext("2d");

// Game variables
let levels = [
    {ball:{x:100,y:550}, hole:{x:700,y:100}, obstacles:[
        {x:300,y:400,w:100,h:20,type:'sand'},
        {x:500,y:250,w:80,h:20,type:'water'}
    ]},
    {ball:{x:50,y:550}, hole:{x:750,y:150}, obstacles:[
        {x:200,y:450,w:120,h:20,type:'sand'},
        {x:400,y:300,w:80,h:20,type:'water'},
        {x:600,y:200,w:100,h:20,type:'sand'}
    ]}
];
let currentLevel = 0;

let ball = {...levels[currentLevel].ball, radius:12};
let hole = {...levels[currentLevel].hole, radius:18};
let obstacles = levels[currentLevel].obstacles;

let velocity = {x:0, y:0};
let moving = false;
let shots = 0;

// Draw function
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
}

// Physics update
function update() {
    if(moving){
        ball.x += velocity.x;
        ball.y += velocity.y;
        velocity.x *= 0.95;
        velocity.y *= 0.95;
        if(Math.abs(velocity.x)<0.5 && Math.abs(velocity.y)<0.5){
            velocity.x = 0;
            velocity.y = 0;
            moving = false;
        }

        // Collision with obstacles
        for(let obs of obstacles){
            if(ball.x+ball.radius > obs.x && ball.x-ball.radius < obs.x+obs.w &&
               ball.y+ball.radius > obs.y && ball.y-ball.radius < obs.y+obs.h){
                // Simple bounce
                velocity.x = -velocity.x*0.5;
                velocity.y = -velocity.y*0.5;
            }
        }
    }
    // Check hole
    let dx = ball.x - hole.x;
    let dy = ball.y - hole.y;
    let dist = Math.sqrt(dx*dx + dy*dy);
    if(dist < ball.radius + hole.radius){
        alert("Hole completed in " + shots + " shots!");
        currentLevel++;
        if(currentLevel >= levels.length){
            alert("所有關卡完成! 總共擊球次數: " + shots);
            currentLevel = 0;
        }
        // Load next level
        ball = {...levels[currentLevel].ball, radius:12};
        hole = {...levels[currentLevel].hole, radius:18};
        obstacles = levels[currentLevel].obstacles;
        shots = 0;
        moving = false;
    }
    document.getElementById("score").innerText = "Shots: " + shots;
    document.getElementById("level").innerText = "Level: " + (currentLevel+1);
    draw();
    requestAnimationFrame(update);
}

// Drag controls
let dragStart = null;
canvas.addEventListener("pointerdown", (e)=>{
    if(!moving){
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

draw();
update();
</script>
"""

st.components.v1.html(html_code, height=700)
