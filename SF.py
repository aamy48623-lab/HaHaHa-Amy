import streamlit as st
from PIL import Image, ImageDraw

# --- Game setup ---
WIDTH, HEIGHT = 400, 400
PLAYER_SIZE = 30
FRAGMENT_SIZE = 20

# Initialize session state
if 'player_x' not in st.session_state:
    st.session_state.player_x = WIDTH // 2
if 'player_y' not in st.session_state:
    st.session_state.player_y = HEIGHT // 2
if 'is_light' not in st.session_state:
    st.session_state.is_light = True
if 'collected' not in st.session_state:
    st.session_state.collected = []
if 'fragment_pos' not in st.session_state:
    st.session_state.fragment_pos = [(50,50), (350,350), (200,200)]

# --- Functions ---
def move(dx, dy):
    st.session_state.player_x = max(0, min(WIDTH - PLAYER_SIZE, st.session_state.player_x + dx))
    st.session_state.player_y = max(0, min(HEIGHT - PLAYER_SIZE, st.session_state.player_y + dy))
    check_collision()

def toggle_light():
    st.session_state.is_light = not st.session_state.is_light

def check_collision():
    for idx, (fx, fy) in enumerate(st.session_state.fragment_pos):
        if idx not in st.session_state.collected:
            if (st.session_state.player_x < fx + FRAGMENT_SIZE and
                st.session_state.player_x + PLAYER_SIZE > fx and
                st.session_state.player_y < fy + FRAGMENT_SIZE and
                st.session_state.player_y + PLAYER_SIZE > fy):
                st.session_state.collected.append(idx)

def draw_game():
    # Create background
    bg_color = (255,255,255) if st.session_state.is_light else (0,0,0)
    player_color = (255,255,100) if st.session_state.is_light else (50,50,50)
    fragment_color = (0,200,255)
    
    img = Image.new('RGB', (WIDTH, HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw fragments
    for idx, (fx, fy) in enumerate(st.session_state.fragment_pos):
        if idx not in st.session_state.collected:
            draw.rectangle([fx, fy, fx+FRAGMENT_SIZE, fy+FRAGMENT_SIZE], fill=fragment_color)
    
    # Draw player
    draw.rectangle([st.session_state.player_x, st.session_state.player_y,
                    st.session_state.player_x+PLAYER_SIZE, st.session_state.player_y+PLAYER_SIZE],
                   fill=player_color)
    
    return img

# --- Streamlit UI ---
st.title("影子碎片 Prototype (Shadow Fragments)")

# Control buttons
col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("↑"):
        move(0, -20)
with col2:
    st.write("Light" if st.session_state.is_light else "Shadow")
    if st.button("Toggle Light/Shadow"):
        toggle_light()
with col3:
    if st.button("↓"):
        move(0, 20)

col4, col5, col6 = st.columns([1,2,1])
with col4:
    if st.button("←"):
        move(-20, 0)
with col5:
    st.write(f"Collected: {len(st.session_state.collected)}/{len(st.session_state.fragment_pos)}")
with col6:
    if st.button("→"):
        move(20, 0)

# Draw game
game_img = draw_game()
st.image(game_img)
