import streamlit as st
import streamlit.components.v1 as components
import time

# 1. SIDEBAR UI (Always visible)
if 'coins' not in st.session_state:
    st.session_state.coins = 0

st.sidebar.title("💳 Mango Wallet")
st.sidebar.metric("Balance", f"{st.session_state.coins} 🥭")

# 2. VERIFICATION TRIGGER
# This catches the "teleport" from Netlify
if st.query_params.get("verified") == "true":
    st.session_state.coins += 10
    # Clear the URL so refreshing doesn't add infinite coins
    st.query_params.clear() 
    st.success("💰 +10 Coins added!")

# 3. THE GAME
st.header("Mango Catcher")
game_js = """
<div id="area" style="width:100%; height:300px; background:#bae6fd; position:relative; overflow:hidden; border-radius:15px;">
    <div id="basket" style="width:60px; height:20px; background:#451a03; position:absolute; bottom:10px; left:50%;"></div>
    <div id="ui" style="position:absolute; top:10px; left:10px; font-weight:bold;">Score: 0</div>
</div>
<script>
    let s = 0; let m = 0;
    const g = document.getElementById('area');
    const b = document.getElementById('basket');
    const lobby = "https://merry-peony-d69278.netlify.app/";

    window.addEventListener('mousemove', (e) => {
        let r = g.getBoundingClientRect();
        b.style.left = (e.clientX - r.left - 30) + 'px';
    });

    function spawn() {
        const mango = document.createElement('div');
        mango.innerHTML = "🥭"; mango.style.position = "absolute"; 
        mango.style.top = "-20px"; mango.style.left = Math.random() * 90 + "%";
        g.appendChild(mango);

        let fall = setInterval(() => {
            let t = parseInt(mango.style.top);
            mango.style.top = (t + 3) + "px"; // Slow Speed

            if(t > 270 && Math.abs(parseInt(mango.style.left) - parseInt(b.style.left)) < 50) {
                s++; document.getElementById('ui').innerText = "Score: " + s;
                mango.remove(); clearInterval(fall);
                if(s >= 10) { 
                    alert("WIN! Redirecting to Ad Lobby..."); 
                    window.parent.location.href = lobby; 
                }
            } else if(t > 300) {
                m++; mango.remove(); clearInterval(fall);
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
components.html(game_js, height=350)
