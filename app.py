import streamlit as st
import streamlit.components.v1 as components
import time

# --- INITIALIZE DATA ---
if 'coins' not in st.session_state:
    st.session_state.coins = 0

st.set_page_config(page_title="Mango Game & Wallet", layout="centered")

# --- SIDEBAR WALLET ---
st.sidebar.title("💰 User Wallet")
st.sidebar.metric("Your Coins", f"{st.session_state.coins} 🥭")
st.sidebar.write(f"Value: ₹{(st.session_state.coins / 480 * 10):.2f}")

tab1, tab2 = st.tabs(["🎮 Play Game", "🏦 Withdraw"])

with tab1:
    st.header("The 10 Mango Challenge")
    st.write("Catch 10 mangoes to win. Miss 3 and you restart!")

    # Difficult Game Script
    game_code = """
    <div id="area" style="width:100%; height:350px; background:#7dd3fc; position:relative; overflow:hidden; border-radius:10px;">
        <div id="basket" style="width:70px; height:30px; background:#78350f; position:absolute; bottom:5px; left:50%; border-radius:0 0 10px 10px;"></div>
        <div id="score" style="position:absolute; top:10px; left:10px; font-weight:bold;">Caught: 0</div>
    </div>
    <script>
        let score = 0; let missed = 0; let basketX = 150;
        const area = document.getElementById('area');
        const basket = document.getElementById('basket');
        const scoreDisp = document.getElementById('score');

        window.addEventListener('mousemove', (e) => {
            let rect = area.getBoundingClientRect();
            basketX = e.clientX - rect.left - 35;
            basket.style.left = basketX + 'px';
        });

        function drop() {
            const m = document.createElement('div');
            m.innerHTML = "🥭"; m.style.position = "absolute"; m.style.top = "-30px";
            m.style.left = Math.random() * (area.clientWidth - 20) + "px";
            area.appendChild(m);
            let fall = setInterval(() => {
                let top = parseInt(m.style.top);
                if(top > 310 && parseInt(m.style.left) > basketX - 10 && parseInt(m.style.left) < basketX + 60) {
                    score++; scoreDisp.innerText = "Caught: " + score;
                    m.remove(); clearInterval(fall);
                    if(score >= 10) { alert("Success! Sending back to claim reward..."); window.parent.location.href = "https://effulgent-sawine-4ed08c.netlify.app/"; }
                } else if(top > 350) {
                    missed++; m.remove(); clearInterval(fall);
                    if(missed >= 3) { alert("Game Over! Try again."); window.parent.location.href = "https://effulgent-sawine-4ed08c.netlify.app/"; }
                } else { m.style.top = (top + 7) + "px"; }
            }, 25);
        }
        setInterval(drop, 800);
    </script>
    """
    components.html(game_code, height=400)
    
    if st.button("Manual Coin Add (For Testing)"):
        st.session_state.coins += 10
        st.rerun()

with tab2:
    st.header("Withdrawal")
    st.warning("Min. Withdrawal: 480 Coins (₹10)")
    
    method = st.selectbox("Method", ["UPI", "GPay", "Redeem Code"])
    id_input = st.text_input("Enter UPI ID or Mobile Number")
    
    if st.button("GET ₹10"):
        if st.session_state.coins < 480:
            st.error(f"Need {480 - st.session_state.coins} more coins!")
        else:
            with st.status("Verifying Coins...") as s:
                time.sleep(2)
                st.write("Checking Ad Impressions...")
                time.sleep(3)
                st.error("❌ ERROR: Payment Gateway Timeout. Coins saved. Try again in 48 hours.")