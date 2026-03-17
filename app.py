import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import time
import random
import string

# --- DATABASE SETUP ---
DB_FILE = "users.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["username", "password", "coins"])
    df.to_csv(DB_FILE, index=False)

def get_users(): return pd.read_csv(DB_FILE)
def save_user(u, p, c):
    df = get_users()
    if u in df['username'].values:
        df.loc[df['username'] == u, 'coins'] = c
    else:
        new_user = pd.DataFrame([[u, p, c]], columns=["username", "password", "coins"])
        df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# --- SESSION STATE ---
if 'user' not in st.session_state: st.session_state.user = None
if 'coins' not in st.session_state: st.session_state.coins = 0

# --- LOGIN / SIGNUP UI ---
if st.session_state.user is None:
    st.title("🥭 Mango Wallet Login")
    choice = st.radio("Select Action", ["Login", "Sign Up"])
    u_input = st.text_input("Username")
    p_input = st.text_input("Password", type="password")
    
    if st.button("Confirm"):
        df = get_users()
        if choice == "Sign Up":
            if u_input in df['username'].values:
                st.error("Username already exists!")
            else:
                save_user(u_input, p_input, 0)
                st.success("Account Created! Please Login.")
        else:
            user_data = df[(df['username'] == u_input) & (df['password'] == p_input)]
            if not user_data.empty:
                st.session_state.user = u_input
                st.session_state.coins = user_data.iloc[0]['coins']
                st.rerun()
            else:
                st.error("Wrong Username or Password")
    st.stop()

# --- LOGGED IN AREA ---
st.sidebar.title(f"👤 {st.session_state.user}")
st.sidebar.metric("Balance", f"{st.session_state.coins} 🥭")
if st.sidebar.button("Logout"):
    save_user(st.session_state.user, "", st.session_state.coins)
    st.session_state.user = None
    st.rerun()

# Capture Ad Verification
if st.query_params.get("verified") == "true":
    st.session_state.coins += 10
    save_user(st.session_state.user, "", st.session_state.coins)
    st.query_params.clear()
    st.success("💰 +10 Coins added!")

tab1, tab2 = st.tabs(["🎮 Play", "🏦 Withdraw"])

with tab1:
    st.header("Mango Catcher")
    game_js = f"""
    <div id="area" style="width:100%; height:300px; background:#e0f2fe; position:relative; overflow:hidden; border-radius:15px;">
        <div id="basket" style="width:60px; height:20px; background:#451a03; position:absolute; bottom:10px; left:50%;"></div>
        <div id="ui" style="position:absolute; top:10px; left:10px; font-weight:bold; color:#0369a1;">Score: 0</div>
    </div>
    <script>
        let s = 0; let m = 0;
        const g = document.getElementById('area');
        const b = document.getElementById('basket');
        const lobby = "https://merry-peony-d69278.netlify.app/";

        window.addEventListener('mousemove', (e) => {{
            let r = g.getBoundingClientRect();
            b.style.left = (e.clientX - r.left - 30) + 'px';
        }});

        function spawn() {{
            const mango = document.createElement('div');
            mango.innerHTML = "🥭"; mango.style.position = "absolute"; 
            mango.style.top = "-20px"; mango.style.left = Math.random() * 90 + "%";
            g.appendChild(mango);

            let fall = setInterval(() => {{
                let t = parseInt(mango.style.top);
                mango.style.top = (t + 3) + "px"; // Slow

                let mRect = mango.getBoundingClientRect();
                let bRect = b.getBoundingClientRect();

                if (mRect.bottom >= bRect.top && mRect.right >= bRect.left && mRect.left <= bRect.right) {{
                    s++; document.getElementById('ui').innerText = "Score: " + s;
                    mango.remove(); clearInterval(fall);
                    if(s >= 10) {{ alert("WIN!"); window.parent.location.href = lobby; }}
                }}
                if(t > 300) {{
                    m++; mango.remove(); clearInterval(fall);
                    if(m >= 3) {{ alert("FAILED!"); window.parent.location.href = lobby; }}
                }}
            }}, 30);
        }}
        setInterval(spawn, 1500);
    </script>
    """
    components.html(game_js, height=350)

with tab2:
    st.header("Withdrawal")
    if st.button("Redeem ₹10 (480 Coins)"):
        if st.session_state.coins >= 480:
            st.warning("⏳ Wait 2 minutes for your code...")
            bar = st.progress(0)
            for i in range(120):
                time.sleep(1)
                bar.progress((i+1)/120)
            code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
            st.session_state.coins -= 480
            save_user(st.session_state.user, "", st.session_state.coins)
            st.success(f"Code: {code}")
