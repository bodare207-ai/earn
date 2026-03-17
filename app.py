import streamlit as st
import pandas as pd
import os
import time
import random
import string
import streamlit.components.v1 as components

st.set_page_config(page_title="Mango Earn", page_icon="🥭")

# --- USER DATABASE ---
DB_FILE = "users.csv"
def get_users():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["username", "password", "coins"])
    return pd.read_csv(DB_FILE)

def save_user_data(u, p, c):
    df = get_users()
    if u in df['username'].values:
        df.loc[df['username'] == u, 'coins'] = c
    else:
        new_row = pd.DataFrame([{"username": u, "password": str(p), "coins": c}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# --- SESSION ---
if 'user' not in st.session_state: st.session_state.user = None
if 'coins' not in st.session_state: st.session_state.coins = 0

# --- LOGIN / SIGNUP ---
if st.session_state.user is None:
    st.title("🥭 Mango Wallet")
    t1, t2 = st.tabs(["Login", "Sign Up"])
    with t1:
        u = st.text_input("User", key="login_u")
        p = st.text_input("Pass", type="password", key="login_p")
        if st.button("Login"):
            df = get_users()
            match = df[(df['username'] == u) & (df['password'].astype(str) == str(p))]
            if not match.empty:
                st.session_state.user = u
                st.session_state.coins = int(match.iloc[0]['coins'])
                st.rerun()
    with t2:
        nu = st.text_input("New User", key="reg_u")
        np = st.text_input("New Pass", type="password", key="reg_p")
        if st.button("Create Account"):
            save_user_data(nu, np, 0)
            st.success("Account Ready! Please Login.")
    st.stop()

# --- COIN CLAIM LOGIC ---
if st.query_params.get("claim") == "8":
    st.session_state.coins += 8
    save_user_data(st.session_state.user, "", st.session_state.coins)
    st.query_params.clear()
    st.balloons()
    st.success("💰 8 Coins Claimed!")

# --- UI ---
st.sidebar.title(f"👤 {st.session_state.user}")
st.sidebar.metric("Coins", f"{st.session_state.coins} 🥭")
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

tab_ads, tab_quiz, tab_game, tab_withdraw = st.tabs(["📺 Watch Ads", "🧠 Quiz", "🎮 Game", "🏦 Withdraw"])

# 1. WATCH ADS
with tab_ads:
    st.header("Direct Ad Rewards")
    st.write("Click to see an ad and earn 8 coins.")
    if st.button("CLICK TO WATCH AD"):
        js = "window.top.location.href = 'https://merry-peony-d69278.netlify.app/';"
        components.html(f"<script>{js}</script>", height=0)

# 2. QUIZ & EARN
with tab_quiz:
    st.header("Brain Quiz")
    q = st.radio("What is 10 + 20?", ["20", "30", "40"])
    if st.button("Submit Answer"):
        if q == "30":
            st.success("Correct! Redirecting to Ad to claim coins...")
            time.sleep(1)
            js = "window.top.location.href = 'https://merry-peony-d69278.netlify.app/';"
            components.html(f"<script>{js}</script>", height=0)
        else:
            st.error("Wrong! Try again.")

# 3. GAME & EARN
with tab_game:
    st.header("Reaction Game")
    st.write("Click the button as fast as you can to win!")
    if st.button("🎯 CLICK TO WIN"):
        st.success("You Won! Loading Ad for reward...")
        time.sleep(1)
        js = "window.top.location.href = 'https://merry-peony-d69278.netlify.app/';"
        components.html(f"<script>{js}</script>", height=0)

# 4. WITHDRAW
with tab_withdraw:
    st.header("Redeem ₹10")
    if st.button("Get Google Play Code (480 Coins)"):
        if st.session_state.coins >= 480:
            st.info("Wait 2 minutes for verification...")
            bar = st.progress(0)
            for i in range(120):
                time.sleep(1)
                bar.progress((i+1)/120)
            code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
            st.session_state.coins -= 480
            save_user_data(st.session_state.user, "", st.session_state.coins)
            st.success(f"Reward: {code}")
        else:
            st.error("Insufficient Coins!")
