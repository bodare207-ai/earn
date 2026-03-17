import streamlit as st
import streamlit.components.v1 as components
import time
import random
import string

# --- CONFIG ---
st.set_page_config(page_title="Mango Wallet", page_icon="🥭", layout="centered")

# --- INITIALIZE STATE ---
if 'coins' not in st.session_state: st.session_state.coins = 0
if 'queue_active' not in st.session_state: st.session_state.queue_active = False
if 'redeem_done' not in st.session_state: st.session_state.redeem_done = False

# 1. VERIFICATION CHECK
# If user comes from Netlify with ?verified=true, they get 10 coins.
if st.query_params.get("verified") == "true":
    st.session_state.coins += 10
    st.query_params.clear() # Prevents refresh-cheating
    st.success("💰 +10 Coins added to your wallet!")

# --- UI TABS ---
tab1, tab2 = st.tabs(["🎮 Play Mango", "🏦 Withdraw"])

with tab1:
    st.header("The 10 Mango Challenge")
    st.write("Catch **10 Small Mangoes**. If you miss 3, you're out!")
    
    # The Game pauses automatically when you switch to Tab 2
    game_js = """
    <div id="g" style="width:100%; height:320px; background:#e0f2fe; position:relative; overflow:hidden; border-radius:15px; border:2px solid #0369a1;">
        <div id="b" style="width:50px; height:15px; background:#451a03; position:absolute; bottom:5px; left:50%; border-radius:3px;"></div>
        <div id="sc" style="position:absolute; top:10px; left:10px; font-weight:bold; color:#0369a1;">Mangoes: 0</div>
    </div>
    <script>
        let s = 0; let m = 0; let bx = 150;
        const g = document.getElementById('g');
        const b = document.getElementById('b');
        const sc = document.getElementById('sc');

        window.addEventListener('mousemove', (e) => {
            let r = g.getBoundingClientRect();
            bx = e.clientX - r.left - 25;
            b.style.left = bx + 'px';
        });

        function spawn() {
            const mango = document.createElement('div');
            mango.innerHTML = "🥭"; mango.style.position = "absolute"; 
            mango.style.top = "-20px"; mango.style.fontSize = "16px"; // Small Mangoes
            mango.style.left = Math.random() * 90 + "%";
            g.appendChild(mango);

            let fall = setInterval(() => {
                let t = parseInt(mango.style.top);
                mango.style.top = (t + 7) + "px"; // Fast Falling
                
                // Hit detection
                if(t > 290 && Math.abs(parseInt(mango.style.left) - bx) < 40) {
                    s++; sc.innerText = "Mangoes: " + s;
                    mango.remove(); clearInterval(fall);
                    if(s >= 10) { 
                        alert("WIN! Redirecting to verify..."); 
                        window.parent.location.href = "https://effulgent-sawine-4ed08c.netlify.app/"; 
                    }
                } else if(t > 320) {
                    m++; mango.remove(); clearInterval(fall);
                    if(m >= 3) { 
                        alert("FAILED! Try again."); 
                        window.parent.location.href = "https://effulgent-sawine-4ed08c.netlify.app/"; 
                    }
                }
            }, 30);
        }
        setInterval(spawn, 900);
    </script>
    """
    if not st.session_state.queue_active:
        components.html(game_js, height=350)
    else:
        st.info("Game paused while withdrawal is in progress.")

with tab2:
    st.header("Withdrawal Center")
    st.sidebar.metric("Your Balance", f"{st.session_state.coins} 🥭")
    
    if not st.session_state.queue_active and not st.session_state.redeem_done:
        st.write("Redeem **480 Coins** for a **₹10 Google Play Code**.")
        method = st.selectbox("Select Method", ["Google Play Code", "UPI", "Amazon Pay"])
        
        if st.button("REDEEM NOW"):
            if st.session_state.coins < 480:
                st.error("Insufficient Coins! You need 480.")
            else:
                st.session_state.queue_active = True
                st.rerun()

    # QUEUE LOGIC
    if st.session_state.queue_active:
        st.warning("⏳ Order processing... You are #4 in queue.")
        st.write("Please wait **2 minutes** for your code to generate.")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for percent_complete in range(100):
            time.sleep(1.2) # Roughly 120 seconds total (2 mins)
            progress_bar.progress(percent_complete + 1)
            status_text.text(f"Queue Progress: {percent_complete + 1}%")
            
        # Code Generation
        new_code = '-'.join([''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(4)])
        st.session_state.coins -= 480
        st.session_state.queue_active = False
        st.session_state.redeem_done = True
        st.session_state.final_code = new_code
        st.rerun()

    if st.session_state.redeem_done:
        st.balloons()
        st.success(f"SUCCESS! Your Redeem Code is: **{st.session_state.final_code}**")
        if st.button("Back to Game"):
            st.session_state.redeem_done = False
            st.rerun()
