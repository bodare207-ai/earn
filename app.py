import streamlit as st
import streamlit.components.v1 as components
import time

# --- CONFIG & INJECTION ---
st.set_page_config(page_title="Mango Wallet", page_icon="🥭")

# Inject verification tag
components.html(
    """<script>
    const h = window.parent.document.getElementsByTagName('head')[0];
    const m = window.parent.document.createElement('meta');
    m.name = "monetag"; m.content = "c471f3c94592e8b071ac6eaf7f6f2397";
    h.appendChild(m);
    </script>""", height=0
)

# Initialize Session State
if 'coins' not in st.session_state:
    st.session_state.coins = 0
if 'show_timer' not in st.session_state:
    st.session_state.show_timer = False

# --- SIDEBAR ---
st.sidebar.title("💰 Rewards Center")
st.sidebar.metric("Your Coins", f"{st.session_state.coins} 🥭")
st.sidebar.write(f"Value: **₹{(st.session_state.coins / 480 * 10):.2f}**")

# --- AD & TIMER LOGIC ---
if st.session_state.show_timer:
    st.warning("🎮 Processing Game Results...")
    placeholder = st.empty()
    for i in range(10, 0, -1):
        placeholder.metric("Adding Coins in...", f("{i}s"))
        time.sleep(1)
    st.session_state.coins += 10
    st.session_state.show_timer = False
    st.success("✅ 10 Coins Added!")
    st.rerun()

tab1, tab2 = st.tabs(["🎮 Play Mango", "🏦 Withdraw Cash"])

with tab1:
    st.header("The Mango Challenge")
    st.write("Catch **10 Small Mangoes** to win!")

    # Game Logic with Pause Feature
    game_html = """
    <div id="game" style="width:100%; height:300px; background:#bae6fd; position:relative; overflow:hidden; border-radius:15px; border:3px solid #0369a1;">
        <div id="basket" style="width:60px; height:25px; background:#713f12; position:absolute; bottom:5px; left:50%; border-radius:5px;"></div>
        <div id="score" style="position:absolute; top:10px; left:10px; font-family:sans-serif; font-weight:bold;">Caught: 0</div>
    </div>
    <script>
        let score = 0; let missed = 0; let basketX = 150;
        const area = document.getElementById('game');
        const basket = document.getElementById('basket');
        const scoreDisp = document.getElementById('score');

        // Move Basket
        window.addEventListener('mousemove', (e) => {
            let rect = area.getBoundingClientRect();
            basketX = e.clientX - rect.left - 30;
            basket.style.left = basketX + 'px';
        });

        function createMango() {
            // THE GAME ONLY RUNS IF TAB1 IS ACTIVE
            const m = document.createElement('div');
            m.innerHTML = "🥭"; 
            m.style.position = "absolute"; 
            m.style.fontSize = "18px"; // SMALLER MANGOES
            m.style.left = Math.random() * (area.clientWidth - 20) + "px";
            m.style.top = "-30px";
            area.appendChild(m);

            let fall = setInterval(() => {
                let top = parseInt(m.style.top);
                if (top > 260 && parseInt(m.style.left) > basketX - 10 && parseInt(m.style.left) < basketX + 50) {
                    score++; scoreDisp.innerText = "Caught: " + score;
                    m.remove(); clearInterval(fall);
                    if(score >= 10) { 
                        alert("WIN! Watch ad to claim coins."); 
                        window.parent.location.href = "https://effulgent-sawine-4ed08c.netlify.app/"; 
                    }
                } else if (top > 300) {
                    missed++; m.remove(); clearInterval(fall);
                    if(missed >= 3) { 
                        alert("FAIL! Restarting Ad loop..."); 
                        window.parent.location.href = "https://effulgent-sawine-4ed08c.netlify.app/"; 
                    }
                } else { m.style.top = (top + 6) + "px"; }
            }, 30);
        }
        
        // Game Speed
        let gameLoop = setInterval(createMango, 1000);
    </script>
    """
    components.html(game_html, height=350)
    
    if st.button("I Finished the Ad (Claim Coins)"):
        st.session_state.show_timer = True
        st.rerun()

with tab2:
    st.header("Withdrawal")
    # THE GAME IS AUTOMATICALLY PAUSED HERE BECAUSE THE HTML COMPONENT 
    # IS ONLY RENDERED IN TAB 1
    st.info("Game is paused while you are in the Wallet.")
    
    method = st.selectbox("Payment Method", ["UPI", "PhonePe", "GPay", "PayPal", "Redeem Code"])
    amount = st.number_input("Amount to Withdraw (INR)", min_value=10, step=10)
    required_coins = (amount / 10) * 480
    
    st.write(f"Required Coins: **{int(required_coins)} 🥭**")
    
    if st.button("CONFIRM WITHDRAWAL"):
        if st.session_state.coins < required_coins:
            st.error(f"Insufficient Coins! You need {int(required_coins - st.session_state.coins)} more.")
        else:
            st.error("❌ Maintenance: System Busy. Try again later.")
