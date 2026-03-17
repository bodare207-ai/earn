import streamlit as st
import streamlit.components.v1 as components
import time
import random
import string

st.set_page_config(page_title="Mango Catcher", layout="centered")

# --- INITIALIZE COINS ---
if 'coins' not in st.session_state: st.session_state.coins = 0

# Check for verification from Lobby
if st.query_params.get("verified") == "true":
    st.session_state.coins += 10
    st.query_params.clear()
    st.success("💰 +10 Coins Added!")

tab1, tab2 = st.tabs(["🎮 Play Game", "🏦 Withdraw"])

with tab1:
    st.header("Slow Mango Challenge")
    st.write("Catch 10 mangoes to win. The mangoes are now **very slow**!")

    game_js = """
    <div id="area" style="width:100%; height:350px; background:#e0f2fe; position:relative; overflow:hidden; border-radius:15px; border:3px solid #0369a1;">
        <div id="basket" style="width:70px; height:20px; background:#451a03; position:absolute; bottom:10px; left:50%; border-radius:5px;"></div>
        <div id="score" style="position:absolute; top:10px; left:10px; font-weight:bold; color:#0369a1;">Score: 0</div>
    </div>
    <script>
        let s = 0; let m = 0; let bx = 150;
        const area = document.getElementById('area');
        const basket = document.getElementById('basket');
        const sc = document.getElementById('score');

        window.addEventListener('mousemove', (e) => {
            let r = area.getBoundingClientRect();
            bx = e.clientX - r.left - 35;
            basket.style.left = bx + 'px';
        });

        function spawn() {
            const mango = document.createElement('div');
            mango.innerHTML = "🥭"; mango.style.position = "absolute"; 
            mango.style.top = "-30px"; mango.style.fontSize = "20px";
            mango.style.left = Math.random() * 90 + "%";
            area.appendChild(mango);

            let fall = setInterval(() => {
                let t = parseInt(mango.style.top);
                // VERY SLOW SPEED: Changed from 7-8 down to 3
                mango.style.top = (t + 3) + "px"; 
                
                // Collision
                if(t > 310 && Math.abs(parseInt(mango.style.left) - bx) < 50) {
                    s++; sc.innerText = "Score: " + s;
                    mango.remove(); clearInterval(fall);
                    if(s >= 10) { 
                        alert("YOU WIN! Redirecting to Ad Lobby..."); 
                        window.parent.location.href = "https://effulgent-sawine-4ed08c.netlify.app/"; 
                    }
                } else if(t > 350) {
                    m++; mango.remove(); clearInterval(fall);
                    if(m >= 3) { 
                        alert("GAME OVER! Redirecting to Ad Lobby..."); 
                        window.parent.location.href = "https://effulgent-sawine-4ed08c.netlify.app/"; 
                    }
                }
            }, 30);
        }
        setInterval(spawn, 1500); // Slower spawn rate too
    </script>
    """
    components.html(game_js, height=400)

with tab2:
    st.header("Withdrawal Center")
    st.metric("Balance", f"{st.session_state.coins} 🥭")
    if st.button("Redeem ₹10 (480 Coins)"):
        if st.session_state.coins >= 480:
            st.info("Queueing request... Wait 2 minutes.")
            bar = st.progress(0)
            for i in range(100):
                time.sleep(1.2)
                bar.progress(i + 1)
            code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
            st.session_state.coins -= 480
            st.success(f"Done! Code: {code}")
        else:
            st.error("Not enough coins!")
