import streamlit as st
import streamlit.components.v1 as components

st.title("影子碎片 (Shadow Fragments) - Real-time Prototype")

# HTML + JS game
game_html = """
<canvas id="gameCanvas" width="400" height="400" style="border:1px solid #000000;"></canvas>
<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let player = {x: 200, y: 200, size: 30};
let isLight = true;
let fragments = [{x:50,y:50},{x:350,y:350},{x:200,y:200}];
let collected = [];

function draw() {
    // Background
    ctx.fillStyle = isLight ? 'white' : 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw fragments
    ctx.fillStyle = 'cyan';
    for(let i=0;i<fragments.length;i++){
        if(!collected.includes(i)){
            ctx.fillRect(fragments[i].x, fragments[i].y, 20, 20);
        }
    }

    // Draw player
    ctx.fillStyle = isLight ? 'yellow' : 'gray';
    ctx.fillRect(player.x, player.y, player.size, player.size);

    // Draw collected count
    ctx.fillStyle = isLight ? 'black' : 'white';
    ctx.font = '16px Arial';
    ctx.fillText('Collected: ' + collected.length + '/' + fragments.length, 10, 20);
}

// Check collisions
function checkCollision() {
    for(let i=0;i<fragments.length;i++){
        if(!collected.includes(i)){
            if(player.x < fragments[i].x + 20 &&
               player.x + player.size > fragments[i].x &&
               player.y < fragments[i].y + 20 &&
               player.y + player.size > fragments[i].y){
                collected.push(i);
            }
        }
    }
}

// Handle key press
document.addEventListener('keydown', function(event){
    const speed = 5;
    if(event.key === 'ArrowUp'){ player.y -= speed; }
    if(event.key === 'ArrowDown'){ player.y += speed; }
    if(event.key === 'ArrowLeft'){ player.x -= speed; }
    if(event.key === 'ArrowRight'){ player.x += speed; }
    if(event.key === ' '){ isLight = !isLight; }
    checkCollision();
});

// Game loop
function gameLoop(){
    draw();
    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>
"""

# Embed the game in Streamlit
components.html(game_html, height=450)

