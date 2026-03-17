import streamlit as st
import streamlit.components.v1 as components
import time
import random
import string

st.set_page_config(page_title="Mango Wallet", page_icon="🥭")

# --- INITIALIZE STATE ---
if 'coins' not in st.session_state: st.session_state.coins = 0
if 'queue_active' not in st.session_state: st.session_state.queue_active = False

# 1. VERIFICATION CHECK: Adds coins only if coming from Netlify
if st.query_params.get("verified") == "true":
    st.session_state.coins += 10
    st.query_params.clear() 
    st.success("💰 +10 Coins added! Your verification was successful.")

tab1, tab2 = st.tabs(["🎮 Play Mango", "🏦 Withdraw"])

with tab1:
    st.header("Mango Challenge")
    
    # Game code with improved redirection
    game_js = """
    <div id="g" style="width:100%; height:300px; background:#e0f2fe; position:relative; overflow:hidden; border-radius:15px;">
        <div id="b" style="width:60px; height:20px; background:#451a03; position:absolute; bottom:5px; left:50%;"></div>
        <div id="score" style="position:absolute; top:10px; left:10px; font-weight:bold; color:#0369a1;">Score: 0</div>
    </div>
    <script>
        let s = 0; let m = 0;
        const g = document.getElementById('g');
        const b = document.getElementById('b');
        const sc = document.getElementById('score');
        const lobby = "https://merry-peony-d69278.netlify.app/";

        window.addEventListener('mousemove', (e) => {
            let r = g.getBoundingClientRect();
            b.style.left = (e.clientX - r.left - 30) + 'px';
        });

        function spawn() {
            const mango = document.createElement('div');
            mango.innerHTML = "🥭"; mango.style.position = "absolute"; 
            mango.style.top = "-20px"; mango.style.fontSize = "20px";
            mango.style.left = Math.random() * 90 + "%";
            g.appendChild(mango);

            let fall = setInterval(() => {
                let t = parseInt(mango.style.top);
                mango.style.top = (t + 3) + "px"; // Slow speed as requested
                
                if(t > 270 && Math.abs(parseInt(mango.style.left) - parseInt(b.style.left)) < 50) {
                    s++; sc.innerText = "Score: " + s;
                    mango.remove(); clearInterval(fall);
                    if(s >= 10) { 
                        alert("WIN! Redirecting to Ad Lobby..."); 
                        window.parent.location.href = lobby; 
                    }
                } else if(t > 300) {
                    m++; mango.remove(); clearInterval(fall);
                    if(m >= 3) { 
                        alert("GAME OVER! Watch ad to retry."); 
                        window.parent.location.href = lobby; 
                    }
                }
            }, 30);
        }
        setInterval(spawn, 1500);
    </script>
    """
    components.html(game_js, height=350)

with tab2:
    st.header("Withdrawal")
    st.metric("Balance", f"{st.session_state.coins} 🥭")
    
    option = st.selectbox("Select Option", ["Redeem Code", "UPI", "GPay"])
    
    if st.button("Claim Reward (480 Coins)"):
        if st.session_state.coins < 480:
            st.error("Not enough coins! You need 480.")
        else:
            st.session_state.queue_active = True
            
    if st.session_state.queue_active:
        st.warning("⏳ Order in Queue... Please wait 2 minutes for your code.")
        bar = st.progress(0)
        for i in range(120):
            time.sleep(1)
            bar.progress((i + 1) / 120)
        
        # Generate Code
        new_code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
        st.session_state.coins -= 480
        st.session_state.queue_active = False
        st.success(f"SUCCESS! Your Code: {new_code}")
