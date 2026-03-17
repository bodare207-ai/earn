import streamlit as st
import streamlit.components.v1 as components
import time
import random
import string

st.set_page_config(page_title="Mango Wallet", layout="centered")

# --- COIN UI & LOGIC ---
if 'coins' not in st.session_state:
    st.session_state.coins = 0

# Check for the verification signal from Netlify
if st.query_params.get("add_now") == "true":
    st.session_state.coins += 10
    st.query_params.clear() # Clear the URL to prevent double-claiming
    st.success("💰 +10 Coins Added! Verification Successful.")
    st.balloons()

# Sidebar UI
st.sidebar.title("💳 Wallet Status")
st.sidebar.metric("Your Balance", f"{st.session_state.coins} 🥭")
st.sidebar.write("---")

tab1, tab2 = st.tabs(["🎮 Play Game", "🏦 Withdraw"])

with tab1:
    st.header("The Slow Mango Challenge")
    
    # Game with AUTO-COUNT and FIXED TELEPORT
    game_html = """
    <div id="area" style="width:100%; height:320px; background:#e0f2fe; position:relative; overflow:hidden; border-radius:15px; border:3px solid #0369a1;">
        <div id="basket" style="width:70px; height:20px; background:#451a03; position:absolute; bottom:10px; left:50%; border-radius:5px;"></div>
        <div id="score_ui" style="position:absolute; top:10px; left:10px; font-weight:bold; font-size:22px; color:#0369a1;">Mangoes: 0</div>
    </div>
    <script>
        let caught = 0; let missed = 0;
        const area = document.getElementById('area');
        const basket = document.getElementById('basket');
        const scoreUI = document.getElementById('score_ui');
        const lobbyURL = "https://merry-peony-d69278.netlify.app/";

        window.addEventListener('mousemove', (e) => {
            let rect = area.getBoundingClientRect();
            let bx = e.clientX - rect.left - 35;
            basket.style.left = bx + 'px';
        });

        function createMango() {
            const m = document.createElement('div');
            m.innerHTML = "🥭"; m.style.position = "absolute"; 
            m.style.top = "-20px"; m.style.left = Math.random() * 90 + "%";
            m.style.fontSize = "20px";
            area.appendChild(m);

            let fall = setInterval(() => {
                let mt = parseInt(m.style.top);
                m.style.top = (mt + 3) + "px"; // Slow Speed

                // AUTO-COUNT: Touching logic
                let mRect = m.getBoundingClientRect();
                let bRect = basket.getBoundingClientRect();

                if (mRect.bottom >= bRect.top && mRect.right >= bRect.left && mRect.left <= bRect.right) {
                    caught++;
                    scoreUI.innerText = "Mangoes: " + caught;
                    m.remove();
                    clearInterval(fall);
                    if(caught >= 10) {
                        alert("WIN! Redirecting to Ad Lobby...");
                        window.parent.location.href = lobbyURL;
                    }
                }

                if (mt > 320) {
                    missed++;
                    m.remove();
                    clearInterval(fall);
                    if(missed >= 3) {
                        alert("FAILED! Redirecting to Lobby...");
                        window.parent.location.href = lobbyURL;
                    }
                }
            }, 30);
        }
        setInterval(createMango, 1800);
    </script>
    """
    components.html(game_html, height=380)

with tab2:
    st.header("Withdrawal")
    st.write("Redeem **480 Coins** for a **₹10 Code**.")
    if st.button("Redeem Now"):
        if st.session_state.coins >= 480:
            st.warning("⏳ Order processing... Please wait 2 minutes.")
            bar = st.progress(0)
            for i in range(120):
                time.sleep(1)
                bar.progress((i+1)/120)
            code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
            st.session_state.coins -= 480
            st.success(f"Success! Your Code: {code}")
        else:
            st.error("Insufficient balance!")
