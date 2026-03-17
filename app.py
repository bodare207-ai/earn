import streamlit as st
import pandas as pd
import os
import time
import random
import string

st.set_page_config(page_title="Mango Wallet", page_icon="🥭")

# --- DATABASE ---
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

# --- LOGIN ---
if st.session_state.user is None:
    st.title("🥭 Mango Wallet")
    t1, t2 = st.tabs(["Login", "Sign Up"])
    with t1:
        u = st.text_input("User")
        p = st.text_input("Pass", type="password")
        if st.button("Login"):
            df = get_users()
            match = df[(df['username'] == u) & (df['password'].astype(str) == str(p))]
            if not match.empty:
                st.session_state.user = u
                st.session_state.coins = int(match.iloc[0]['coins'])
                st.rerun()
    with t2:
        nu = st.text_input("New User")
        np = st.text_input("New Pass", type="password")
        if st.button("Create"):
            save_user_data(nu, np, 0)
            st.success("Created! Log in.")
    st.stop()

# --- MAIN APP ---
st.sidebar.title(f"👤 {st.session_state.user}")
st.sidebar.metric("Balance", f"{st.session_state.coins} 🥭")

# 20% CUT LOGIC: User gets 8 coins per ad
if st.query_params.get("claim") == "8":
    st.session_state.coins += 8
    save_user_data(st.session_state.user, "", st.session_state.coins)
    st.query_params.clear()
    st.balloons()
    st.success("💰 8 Coins added to your wallet!")

st.header("Earn Coins")
st.write("Click the button below to watch an ad and earn **8 Mango Coins**.")

# The Breakout Button (No more game!)
if st.button("📺 WATCH AD TO EARN"):
    js = "window.top.location.href = 'https://merry-peony-d69278.netlify.app/';"
    st.components.v1.html(f"<script>{js}</script>", height=0)

st.divider()

# Withdrawal
st.subheader("Redeem Rewards")
if st.button("Redeem ₹10 (480 Coins)"):
    if st.session_state.coins >= 480:
        st.info("⏳ Validating... Wait 2 mins.")
        bar = st.progress(0)
        for i in range(120):
            time.sleep(1)
            bar.progress((i+1)/120)
        code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
        st.session_state.coins -= 480
        save_user_data(st.session_state.user, "", st.session_state.coins)
        st.success(f"SUCCESS! Your Code: {code}")
    else:
        st.error(f"Need {480 - st.session_state.coins} more coins.")
