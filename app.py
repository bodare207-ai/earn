import streamlit as st
import streamlit.components.v1 as components
import time
import random
import string

st.set_page_config(page_title="Mango Wallet", page_icon="🥭")

# --- COIN LOGIC ---
if 'coins' not in st.session_state: st.session_state.coins = 0
if 'in_queue' not in st.session_state: st.session_state.in_queue = False

# Capture teleport from Netlify and add coins
params = st.query_params
if params.get("add_coins") == "true":
    st.session_state.coins += 10
    st.query_params.clear() # Clear URL so refresh doesn't add more coins
    st.toast("💰 10 Coins added to your wallet!")

tab1, tab2 = st.tabs(["🎮 Play Game", "🏦 Withdraw"])

with tab1:
    st.header("Mango Challenge")
    
    # Very slow mangoes + Auto-teleport logic
    game_js = """
    <div id="g" style="width:100%; height:300px; background:#e0f2fe; position:relative; overflow:hidden; border-radius:15px; border:2px solid #0369a1;">
        <div id="b" style="width:60px; height:20px; background:#451a03; position:absolute; bottom:5px; left:50%; border-radius:5px;"></div>
        <div id="sc" style="position:absolute; top:10px; left:10px; font-weight:bold; color:#0369a1;">Score: 0</div>
    </div>
    <script>
        let s = 0; let m = 0;
        const g = document.getElementById('g');
        const b = document.getElementById('b');
        const sc = document.getElementById('sc');
        const lobbyURL = "https://merry-peony-d69278.netlify.app/";

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
                mango.style.top = (t + 3) + "px"; // VERY SLOW
                
                // Hit Logic
                if(t > 270 && Math.abs(parseInt(mango.style.left) - parseInt(b.style.left)) < 50) {
                    s++; sc.innerText = "Score: " + s;
                    mango.remove(); clearInterval(fall);
                    if(s >= 10) { 
                        alert("WIN! Redirecting to Ad Lobby..."); 
                        window.parent.location.href = lobbyURL; 
                    }
                } else if(t > 300) {
                    m++; mango.remove(); clearInterval(fall);
                    if(m >= 3) { 
                        alert("FAILED! Redirecting to Lobby..."); 
                        window.parent.location.href = lobbyURL; 
                    }
                }
            }, 30);
        }
        setInterval(spawn, 1500);
    </script>
    """
    components.html(game_js, height=350)

with tab2:
    st.header("Withdrawal Settings")
    st.metric("Balance", f"{st.session_state.coins} 🥭")
    
    withdraw_type = st.selectbox("Choose Method", ["Redeem Code", "UPI Cash Out"])
    
    if st.button("Claim Reward (480 Coins)"):
        if st.session_state.coins < 480:
            st.error("Insufficient Balance. You need 480 Coins.")
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
        st.balloons()
        st.success(f"SUCCESS! Your Redeem Code: **{code}**")
