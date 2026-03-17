import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import time
import random
import string

# --- DATABASE SETUP ---
DB_FILE = "users.csv"

# Function to load users safely
def get_users():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["username", "password", "coins"])
    return pd.read_csv(DB_FILE)

# Function to save/update users
def save_user_data(u, p, c, is_new=False):
    df = get_users()
    if u in df['username'].values:
        # Update existing user's coins
        df.loc[df['username'] == u, 'coins'] = c
    else:
        # Add brand new user
        new_row = pd.DataFrame([{"username": u, "password": p, "coins": c}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# --- SESSION STATE ---
if 'user' not in st.session_state: st.session_state.user = None
if 'coins' not in st.session_state: st.session_state.coins = 0

# --- LOGIN / SIGNUP UI ---
if st.session_state.user is None:
    st.title("🥭 Mango Wallet")
    
    # Use tabs for a cleaner Login/Signup UI
    tab_auth1, tab_auth2 = st.tabs(["Login", "Sign Up"])
    
    with tab_auth1:
        u_log = st.text_input("Username", key="log_u")
        p_log = st.text_input("Password", type="password", key="log_p")
        if st.button("Login"):
            df = get_users()
            # Strict check for both username and password
            user_match = df[(df['username'] == u_log) & (df['password'].astype(str) == str(p_log))]
            if not user_match.empty:
                st.session_state.user = u_log
                st.session_state.coins = int(user_match.iloc[0]['coins'])
                st.success(f"Welcome back, {u_log}!")
                st.rerun()
            else:
                st.error("❌ Wrong Username or Password. Please check carefully.")

    with tab_auth2:
        u_sign = st.text_input("Choose Username", key="sign_u")
        p_sign = st.text_input("Choose Password", type="password", key="sign_p")
        if st.button("Create Account"):
            df = get_users()
            if u_sign in df['username'].values:
                st.warning("This username is already taken!")
            elif u_sign == "" or p_sign == "":
                st.error("Please fill in both fields!")
            else:
                save_user_data(u_sign, p_sign, 0, is_new=True)
                st.success("✅ Account Created Successfully! Now go to the Login tab.")
    
    st.stop() # Stop here if not logged in

# --- LOGGED IN AREA ---
st.sidebar.title(f"👤 {st.session_state.user}")
st.sidebar.metric("Balance", f"{st.session_state.coins} 🥭")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# Capture Ad Verification from Lobby
if st.query_params.get("verified") == "true":
    st.session_state.coins += 10
    save_user_data(st.session_state.user, "", st.session_state.coins) # Sync coins to CSV
    st.query_params.clear()
    st.toast("💰 +10 Coins added!")

# --- GAME & WITHDRAW TABS ---
t1, t2 = st.tabs(["🎮 Play", "🏦 Withdraw"])

with t1:
    # (Insert your slow mango game HTML here - Same as before)
    st.write("Game is ready. Catch 10 mangoes!")
    # ... [Game HTML Component] ...

with t2:
    st.header("Withdrawal")
    if st.button("Redeem ₹10 (480 Coins)"):
        if st.session_state.coins >= 480:
            st.warning("⏳ Order in Queue... Wait 2 minutes.")
            bar = st.progress(0)
            for i in range(120):
                time.sleep(1)
                bar.progress((i+1)/120)
            
            # 16-digit fake code generator
            code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
            st.session_state.coins -= 480
            save_user_data(st.session_state.user, "", st.session_state.coins) # Sync balance
            st.success(f"Redeem Successful! Code: {code}")
        else:
            st.error(f"You need {480 - st.session_state.coins} more coins.")
