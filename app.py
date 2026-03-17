import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import time
import random
import string

# --- CONFIG ---
st.set_page_config(page_title="Mango Wallet", page_icon="🥭", layout="centered")

# --- DATABASE SETUP ---
DB_FILE = "users.csv"

def get_users():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["username", "password", "coins"])
    return pd.read_csv(DB_FILE)

def save_user_data(u, p, c):
    df = get_users()
    # If password is empty (syncing coins), keep the old password
    if u in df['username'].values:
        df.loc[df['username'] == u, 'coins'] = c
    else:
        new_row = pd.DataFrame([{"username": u, "password": str(p), "coins": c}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

# --- SESSION STATE ---
if 'user' not in st.session_state: st.session_state.user = None
if 'coins' not in st.session_state: st.session_state.coins = 0

# --- AUTHENTICATION INTERFACE ---
if st.session_state.user is None:
    st.title("🥭 Mango Wallet")
    st.write("Login to save your coins and earn rewards!")
    
    t1, t2 = st.tabs(["Login", "Sign Up"])
    
    with t1:
        u_log = st.text_input("Username", key="l_u")
        p_log = st.text_input("Password", type="password", key="l_p")
        if st.button("Login Now"):
            df = get_users()
            # Ensure password comparison is done as strings
            match = df[(df['username'] == u_log) & (df['password'].astype(str) == str(p_log))]
            if not match.empty:
                st.session_state.user = u_log
                st.session_state.coins = int(match.iloc[0]['coins'])
                st.success(f"Welcome, {u_log}!")
                st.rerun()
            else:
                st.error("❌ Invalid Username or Password")

    with t2:
        u_sign = st.text_input("New Username", key="s_u")
        p_sign = st.text_input("New Password", type="password", key="s_p")
        if st.button("Create Account"):
            df = get_users()
            if u_sign in df['username'].values:
                st.warning("Username already taken!")
            elif u_sign and p_sign:
                save_user_data(u_sign, p_sign, 0)
                st.success("✅ Account Created! Now please Login.")
            else:
                st.error("Please fill in both fields!")
    st.stop()

# --- LOGGED IN DASHBOARD ---
st.sidebar.title(f"👤 {st.session_state.user}")
st.sidebar.metric("Balance", f"{st.session_state.coins} 🥭")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# Check for Ad Verification from Lobby
if st.query_params.get("verified") == "true":
    st.session_state.coins += 10
    save_user_data(st.session_state.user, "", st.session_state.coins)
    st.query_params.clear()
    st.toast("💰 +10 Coins Added!")
    st.balloons()

# --- MAIN TABS ---
tab_game, tab_draw = st.tabs(["🎮 Play Game", "🏦 Withdraw"])

with tab_game:
    st.subheader("Catch 10 Mangoes to Earn!")
    st.info("Win or Lose = Redirect to Ad Lobby to claim coins.")
    
    # THE GAME COMPONENT WITH TELEPORT FIX
    game_html = """
    <div id="game" style="width:100%; height:350px; background:#e0f2fe; position:relative; overflow:hidden; border-radius:15px; border:3px solid #0369a1; cursor:crosshair;">
        <div id="basket" style="width:75px; height:25px; background:#451a03; position:absolute; bottom:10px; left:50%; border-radius:5px; transition: 0.1s;"></div>
        <div id="score" style="position:absolute; top:10px; left:10px; font-weight:bold; font-size:22px; color:#0369a1; font-family: sans-serif;">Score: 0</div>
    </div>
    <script>
        let s = 0; let m = 0;
        const g = document.getElementById('game');
        const b = document.getElementById('basket');
        const sc = document.getElementById('score');
        const lobby = "https://merry-peony-d69278.netlify.app/";

        window.addEventListener('mousemove', (e) => {
            let rect = g.getBoundingClientRect();
            let bx = e.clientX - rect.left - 37;
            if(bx < 0) bx = 0;
            if(bx > rect.width - 75) bx = rect.width - 75;
            b.style.left = bx + 'px';
        });

        function spawn() {
            const mango = document.createElement('div');
            mango.innerHTML = "🥭"; 
            mango.style.position = "absolute"; 
            mango.style.top = "-30px"; 
            mango.style.left = Math.random() * 90 + "%";
            mango.style.fontSize = "25px";
            g.appendChild(mango);

            let fall = setInterval(() => {
                let t = parseInt(mango.style.top);
                mango.style.top = (t + 3) + "px"; // Slow Speed

                let mR = mango.getBoundingClientRect();
                let bR = b.getBoundingClientRect();

                // COLLISION LOGIC
                if (mR.bottom >= bR.top && mR.right >= bR.left && mR.left <= bR.right) {
                    s++; sc.innerText = "Score: " + s;
                    mango.remove(); clearInterval(fall);
                    if(s >= 10) { 
                        alert("WIN! Teleporting to Lobby..."); 
                        window.parent.location.href = lobby; 
                    }
                }
                
                // MISS LOGIC
                if(t > 330) {
                    m++; 
                    mango.remove(); 
                    clearInterval(fall);
                    if(m >= 3) { 
                        alert("FAILED! Redirecting to Lobby..."); 
                        window.parent.location.href = lobby; 
                    }
                }
            }, 30);
        }
        setInterval(spawn, 1500);
    </script>
    """
    components.html(game_html, height=400)

with tab_draw:
    st.header("Withdrawal")
    st.write("Minimum Redeem: **480 Coins** for **₹10 Code**.")
    
    if st.button("Redeem Reward"):
        if st.session_state.coins >= 480:
            st.warning("⏳ Order in Queue... Code will generate in 2 minutes.")
            p = st.progress(0)
            for i in range(120):
                time.sleep(1)
                p.progress((i+1)/120)
            
            # Generate fake code
            code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
            st.session_state.coins -= 480
            save_user_data(st.session_state.user, "", st.session_state.coins)
            st.success(f"SUCCESS! Your Reward Code: **{code}**")
        else:
            st.error(f"Not enough coins. You need {480 - st.session_state.coins} more!")
