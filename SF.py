import streamlit as st
import time
import random

st.set_page_config(page_title="躲避障礙小方塊", layout="centered")

# 遊戲初始化
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 2  # 玩家初始位置 (0~4)
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "game_over" not in st.session_state:
    st.session_state.game_over = False

GRID_WIDTH = 5
GRID_HEIGHT = 10

# 玩家控制
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("←") and not st.session_state.game_over:
        st.session_state.player_pos = max(0, st.session_state.player_pos - 1)
with col3:
    if st.button("→") and not st.session_state.game_over:
        st.session_state.player_pos = min(GRID_WIDTH-1, st.session_state.player_pos + 1)

# 障礙物生成
if not st.session_state.game_over:
    if random.random() < 0.5:  # 每次更新有50%機率生成障礙
        st.session_state.obstacles.append([random.randint(0, GRID_WIDTH-1), 0])

# 障礙物移動
new_obstacles = []
for obs in st.session_state.obstacles:
    obs[1] += 1  # 往下移
    if obs[1] < GRID_HEIGHT:
        new_obstacles.append(obs)
st.session_state.obstacles = new_obstacles

# 碰撞檢測
for obs in st.session_state.obstacles:
    if obs[1] == GRID_HEIGHT-1 and obs[0] == st.session_state.player_pos:
        st.session_state.game_over = True

# 顯示網格
grid = [["⬜" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
for obs in st.session_state.obstacles:
    grid[obs[1]][obs[0]] = "🟥"
grid[GRID_HEIGHT-1][st.session_state.player_pos] = "🟦"  # 玩家

for row in grid:
    st.write("".join(row))

# 分數與關卡
if not st.session_state.game_over:
    st.session_state.score += 1
    if st.session_state.score % 20 == 0:  # 每20分升一關
        st.session_state.level += 1

st.write(f"分數: {st.session_state.score}  |  關卡: {st.session_state.level}")

# 遊戲結束
if st.session_state.game_over:
    st.write("💥 遊戲結束！刷新頁面重新開始。")

# 自動刷新
if not st.session_state.game_over:
    time.sleep(max(0.1, 0.5 - st.session_state.level*0.03))
    st.experimental_rerun()
