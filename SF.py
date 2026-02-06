import streamlit as st
import streamlit.components.v1 as components

st.title("🌀 Gravity Shift｜重力錯亂")

html = """
<canvas id="g" width="500" height="400"></canvas>
<script>
const c = document.getElementById("g");
const ctx = c.getContext("2d");

let p = {x:240,y:50,s:25,vx:0,vy:0};
let gravity = "down";
let speed = 0.5;
let alive = true;
let score = 0;

let orbs = [{x:200,y:200},{x:400,y:300}];

document.addEventListener("keydown",e=>{
  if(e.key==="ArrowLeft") p.vx=-3;
  if(e.key==="ArrowRight") p.vx=3;
  if(e.key===" ") toggleGravity();
});
document.addEventListener("keyup",()=>p.vx=0);

function toggleGravity(){
  gravity = gravity==="down"?"right":
            gravity==="right"?"up":
            gravity==="up"?"left":"down";
}

function update(){
  if(!alive) return;

  if(gravity==="down") p.vy+=speed;
  if(gravity==="up") p.vy-=speed;
  if(gravity==="right") p.vx+=speed;
  if(gravity==="left") p.vx-=speed;

  p.x+=p.vx;
  p.y+=p.vy;

  // walls
  if(p.x<0||p.x>475||p.y<0||p.y>375){
    alive=false;
  }

  // orbs
  orbs = orbs.filter(o=>{
    if(Math.abs(p.x-o.x)<20 && Math.abs(p.y-o.y)<20){
      score++;
      speed+=0.1;
      return false;
    }
    return true;
  });
}

function draw(){
  ctx.fillStyle="#111";
  ctx.fillRect(0,0,500,400);

  // orbs
  ctx.fillStyle="lime";
  orbs.forEach(o=>ctx.fillRect(o.x,o.y,15,15));

  // player
  ctx.fillStyle=alive?"cyan":"red";
  ctx.fillRect(p.x,p.y,p.s,p.s);

  ctx.fillStyle="white";
  ctx.fillText("Score: "+score,10,20);
  ctx.fillText("Gravity: "+gravity,10,40);
  if(!alive) ctx.fillText("GAME OVER",200,200);
}

function loop(){
  update();
  draw();
  requestAnimationFrame(loop);
}
loop();
</script>
"""

components.html(html, height=450)
