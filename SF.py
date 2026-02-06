import streamlit as st
import streamlit.components.v1 as components

st.title("🎵 Beat Rift｜節奏裂縫")

html = """
<canvas id="b" width="520" height="400"></canvas>
<script>
const c = document.getElementById("b");
const ctx = c.getContext("2d");

let p = {x:240,y:330,s:20};
let phase = 0;
let beat = false;
let score = 0;

let cores = [
  {x:120,y:200},
  {x:260,y:160},
  {x:400,y:220}
];

document.addEventListener("keydown",e=>{
  if(e.key==="ArrowLeft") p.x-=10;
  if(e.key==="ArrowRight") p.x+=10;

  if(e.key===" "){
    if(beat){
      score++;
    }else{
      p.x=240; // miss beat → reset
    }
  }
});

function loop(){
  phase += 0.05;
  beat = Math.sin(phase) > 0.95;

  // background pulse
  let pulse = (Math.sin(phase)+1)/2 * 30;
  ctx.fillStyle = "rgb("+(20+pulse)+",20,40)";
  ctx.fillRect(0,0,520,400);

  // beat zone
  ctx.fillStyle = beat ? "lime":"#333";
  ctx.fillRect(0,300,520,20);

  // cores
  ctx.fillStyle = "violet";
  cores = cores.filter(o=>{
    if(Math.abs(p.x-o.x)<15 && Math.abs(p.y-o.y)<15){
      score+=2;
      return false;
    }
    ctx.fillRect(o.x,o.y,12,12);
    return true;
  });

  // player
  ctx.fillStyle = "cyan";
  ctx.fillRect(p.x,p.y,p.s,p.s);

  ctx.fillStyle="white";
  ctx.fillText("Score: "+score,10,20);
  ctx.fillText("SPACE = Beat",10,40);

  requestAnimationFrame(loop);
}
loop();
</script>
"""

components.html(html, height=460)
