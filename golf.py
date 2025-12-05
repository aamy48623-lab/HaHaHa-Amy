# Gunfight — a quick-draw reaction game for Streamlit
# Save this file as `gunfight_streamlit.py` and run:
#    streamlit run gunfight_streamlit.py

import streamlit as st
import time
import random
from math import floor

st.set_page_config(page_title="Gunfight — Quick Draw", layout="centered")

# --- Helper functions -----------------------------------------------------

def now_ms():
    return time.time()


def reset_round(state):
    state['phase'] = 'idle'         # idle, preparing, ready, drawn, result
    state['can_draw'] = False
    state['signal_time'] = None
    state['draw_time_player'] = None
    state['draw_time_cpu'] = None
    state['result_text'] = ''


# --- initialize session state --------------------------------------------
if 'round' not in st.session_state:
    st.session_state.round = 1
if 'score_player' not in st.session_state:
    st.session_state.score_player = 0
if 'score_cpu' not in st.session_state:
    st.session_state.score_cpu = 0
if 'phase' not in st.session_state:
    reset_round(st.session_state)

# --- layout ---------------------------------------------------------------
st.title("🔫 Gunfight — Quick Draw")
st.write(
    "Be the fastest gunslinger! Wait for the 'DRAW!' signal, then press **Draw**. "
    "If you shoot too early you lose the round. Play against the CPU or practice by yourself."
)

col1, col2 = st.columns([2,1])
with col2:
    st.metric("Round", st.session_state.round)
    st.metric("Your score", st.session_state.score_player)
    st.metric("CPU score", st.session_state.score_cpu)

with col1:
    difficulty = st.slider("CPU difficulty (lower = faster)", 0.5, 2.0, 1.0, 0.05)
    variance = st.slider("CPU variability (reaction spread)", 0.01, 0.6, 0.12, 0.01)
    prep_min, prep_max = st.slider("Signal delay range (seconds)", 0.5, 4.0, (1.0, 2.5), 0.1)
    best_of = st.selectbox("Match length", [1,3,5,7], index=1)

st.write("---")

# --- controls and display area -------------------------------------------
placeholder = st.empty()
controls = st.empty()

# Buttons: Start round, Draw (disabled until signal), Reset match
colA, colB, colC = controls.beta_columns(3)
start_btn = colA.button("Start round")
# 'Draw' button: we need to capture presses even when disabled; we'll show text instead when not callable
draw_btn = colB.button("Draw")
reset_match_btn = colC.button("Reset match")

# Reset match
if reset_match_btn:
    st.session_state.round = 1
    st.session_state.score_player = 0
    st.session_state.score_cpu = 0
    reset_round(st.session_state)

# Start a round
if start_btn and st.session_state.phase == 'idle':
    st.session_state.phase = 'preparing'
    st.session_state.can_draw = False
    # choose random delay before signal
    st.session_state._signal_delay = random.uniform(prep_min, prep_max)
    st.session_state._prep_start = now_ms()
    st.experimental_rerun()

# Player pressing draw
if draw_btn:
    # If player cannot draw yet => early shot
    if not st.session_state.can_draw:
        # early shot
        st.session_state.draw_time_player = now_ms()
        st.session_state.phase = 'result'
        st.session_state.result_text = "You shot too early! CPU wins this round."
        st.session_state.score_cpu += 1
        st.session_state.round += 1
        reset_round(st.session_state)
        st.experimental_rerun()
    else:
        # valid draw — record reaction time
        st.session_state.draw_time_player = now_ms()
        st.session_state.phase = 'drawn'
        # CPU reaction simulation
        cpu_reaction = max(0.02, random.gauss(0.25 * difficulty, variance))
        # CPU cannot beat physical impossibility: if cpu_reaction < 0 => guard
        st.session_state.draw_time_cpu = st.session_state.signal_time + cpu_reaction
        # determine winner
        player_rt = st.session_state.draw_time_player - st.session_state.signal_time
        cpu_rt = st.session_state.draw_time_cpu - st.session_state.signal_time
        # tiny rounding
        player_rt = max(0.0, player_rt)
        cpu_rt = max(0.0, cpu_rt)
        if abs(player_rt - cpu_rt) < 0.0001:
            st.session_state.result_text = f"Tie! Both fired at {player_rt:.3f}s"
        elif player_rt < cpu_rt:
            st.session_state.result_text = f"You win! Your reaction: {player_rt:.3f}s vs CPU {cpu_rt:.3f}s"
            st.session_state.score_player += 1
        else:
            st.session_state.result_text = f"CPU wins. Your reaction: {player_rt:.3f}s vs CPU {cpu_rt:.3f}s"
            st.session_state.score_cpu += 1
        st.session_state.round += 1
        reset_round(st.session_state)
        st.experimental_rerun()

# --- Main animation / game loop logic (driven by reruns) -----------------
with placeholder.container():
    if st.session_state.phase == 'idle':
        st.subheader("Ready for the next round")
        st.info("Click **Start round** to begin. Don't press **Draw** until you see 'DRAW!'")
    elif st.session_state.phase == 'preparing':
        st.subheader("Get ready...")
        # show a short countdown to the random signal using time.sleep and rerun
        elapsed = now_ms() - st.session_state._prep_start
        remaining = st.session_state._signal_delay - elapsed
        if remaining > 0:
            st.write(f"Signal in ~{remaining:.2f} seconds")
            # wait a small step then rerun to update countdown
            time.sleep(0.05)
            st.experimental_rerun()
        else:
            # signal now
            st.session_state.phase = 'ready'
            st.session_state.can_draw = True
            st.session_state.signal_time = now_ms()
            st.experimental_rerun()
    elif st.session_state.phase == 'ready':
        st.markdown("<h1 style='color: red;'>DRAW!</h1>", unsafe_allow_html=True)
        st.write("Click **Draw** now!")
        # keep UI waiting for player to click Draw; we also start CPU timer
        # If the user never clicks, we can auto-resolve after a timeout so the game moves on
        # Auto-resolve after 3 seconds: CPU always fires
        if 'signal_time' in st.session_state and st.session_state.signal_time:
            if now_ms() - st.session_state.signal_time > 3.0:
                # CPU fires automatically
                cpu_reaction = max(0.02, random.gauss(0.25 * difficulty, variance))
                st.session_state.draw_time_cpu = st.session_state.signal_time + cpu_reaction
                st.session_state.phase = 'result'
                player_rt = float('inf')
                cpu_rt = st.session_state.draw_time_cpu - st.session_state.signal_time
                st.session_state.result_text = f"CPU fired after {cpu_rt:.3f}s — you didn't react in time."
                st.session_state.score_cpu += 1
                st.session_state.round += 1
                reset_round(st.session_state)
                st.experimental_rerun()
    elif st.session_state.phase == 'drawn':
        st.write("Round resolved — showing results...")
    elif st.session_state.phase == 'result':
        st.write(st.session_state.result_text)

# --- Match end check -----------------------------------------------------
if st.session_state.score_player >= (best_of // 2 + 1) or st.session_state.score_cpu >= (best_of // 2 + 1):
    winner = "You" if st.session_state.score_player > st.session_state.score_cpu else "CPU"
    st.success(f"Match over — {winner} won the best-of-{best_of} match!")
    if st.button("Reset match to play again"):
        st.session_state.round = 1
        st.session_state.score_player = 0
        st.session_state.score_cpu = 0
        reset_round(st.session_state)

# --- Footer / tips -------------------------------------------------------
st.write("---")
st.caption("Tip: close the developer tools and maximize your browser for the best reaction testing — browser UI and latency can affect timings.")

# End of file
