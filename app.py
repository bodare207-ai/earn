import streamlit as st
import streamlit.components.v1 as components
import time
import random
import string

st.set_page_config(page_title="Mango Wallet", page_icon="🥭", layout="centered")

# --- INITIALIZE STATE & UI ---
if 'coins' not in st.session_state: st.session_state.coins = 0
if 'in_queue' not in st.session_state: st.session_state.in_queue = False

# Sidebar UI to see coins
st.sidebar.title("💳 Your Wallet")
st.sidebar.metric("Total Coins", f"{st.session_state.coins} 🥭")
st.sidebar.write("---")

# Capture verification from Netlify
params = st.query_params
if params.get("verified") == "true":
    st.session_state.coins += 10
    st.query_params.clear() 
    st.toast("💰 +10 Coins added successfully!")
    st.balloons()

tab1, tab2 = st.tabs(["🎮 Play Game", "🏦 Withdraw"])

with tab1:
    st.header("Mango Catcher")
    st.write("Catch **10 Mangoes** to win. If you miss 3, you lose!")
    
    # Game with Fixed Collision and Teleport
    game_js = """
    <div id="area" style="width:100%; height:300px; background:#bae6fd; position:relative; overflow:hidden; border-radius:15px; border:3px solid #0369a1;">
        <div id="basket" style="width:60px; height:20px; background:#451a03; position:absolute; bottom:10px; left:50%; border-radius:5px;"></div>
        <div id="score_ui" style="position:absolute; top:10px; left:10px; font-weight:bold; font-size:20px; color:#0369a1;">Score: 0</div>
    </div>
    <script>
        let score = 0; let missed = 0;
        const area = document.getElementById('area');
        const basket = document.getElementById('basket');
        const scoreUI = document.getElementById('score_ui');
        const lobby = "https://merry-peony-d69278.netlify.app/";

        window.addEventListener('mousemove', (e) => {
            let rect = area.getBoundingClientRect();
            let bx = e.clientX - rect.left - 30;
            basket.style.left = bx + 'px';
        });

        function spawn() {
            const m = document.createElement('div');
            m.innerHTML = "🥭"; m.style.position = "absolute"; 
            m.style.top = "-20px"; m.style.left = Math.random() * 90 + "%";
            area.appendChild(m);

            let fall = setInterval(() => {
                let mt = parseInt(m.style.top);
                m.style.top = (mt + 3) + "px"; // Slow falling

                // COLLISION LOGIC: Mango touches basket
                let mRect = m.getBoundingClientRect();
                let bRect = basket.getBoundingClientRect();

                if (mRect.bottom >= bRect.top && mRect.right >= bRect.left && mRect.left <= bRect.right) {
                    score++;
                    scoreUI.innerText = "Score: " + score;
                    m.remove();
                    clearInterval(fall);
                    if(score >= 10) {
                        alert("WIN! Redirecting to Ad Lobby...");
                        window.parent.location.href = lobby;
                    }
                }

                if (mt > 300) {
                    missed++;
                    m.remove();
                    clearInterval(fall);
                    if(missed >= 3) {
                        alert("FAILED! Redirecting to Lobby...");
                        window.parent.location.href = lobby;
                    }
                }
            }, 30);
        }
        setInterval(spawn, 1500);
    </script>
    """
    if not st.session_state.in_queue:
        components.html(game_js, height=350)

with tab2:
    st.header("Withdrawal Settings")
    st.write(f"Current Balance: **{st.session_state.coins} Coins**")
    
    withdraw_method = st.selectbox("Select Method", ["Redeem Code", "UPI Cash"])
    
    if st.button("Claim ₹10 Reward (480 Coins)"):
        if st.session_state.coins < 480:
            st.error("Insufficient Coins! You need at least 480.")
        else:
            st.session_state.in_queue = True
            
    if st.session_state.in_queue:
        st.warning("⏳ Order in Queue... Generating code in 2 minutes.")
        progress = st.progress(0)
        for i in range(120): # 120 seconds
            time.sleep(1)
            progress.progress((i + 1) / 120)
        
        # Generation Logic
        code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
        st.session_state.coins -= 480
        st.session_state.in_queue = False
        st.success(f"SUCCESS! Your Redeem Code: **{code}**")
