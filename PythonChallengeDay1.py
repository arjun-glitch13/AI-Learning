import streamlit as st

st.set_page_config(page_title="Python Challenge Day 1", page_icon="🐞", layout="centered")

st.markdown("""
<style>
/* Darker red background with polka dots */
.stApp {
  background:
    radial-gradient(circle at 20px 20px, rgba(255,255,255,0.15) 2.5px, transparent 3px) 0 0/40px 40px,
    radial-gradient(circle at 10px 10px, rgba(255,255,255,0.08) 2px, transparent 2.5px) 0 0/20px 20px,
    #b71c1c; /* darker red */
}
h1, .stMarkdown h1 { color: #ffffff !important; }
.stButton>button {
  background: #ffffff !important;
  color: #b71c1c !important;
  border-radius: 10px;
  font-weight: 600;
}

/* Black slider handle and track */
[data-testid="stSlider"] > div > div > div > div {
  background-color: #000000 !important;
}
[data-testid="stSlider"] > div > div > div > div[role="slider"] {
  background-color: #000000 !important;
  border: 2px solid #fff !important;
}

/* Ladybug styling */
.ladybug {
  position: fixed;
  right: 20px;
  bottom: 20px;
  width: 130px;
  z-index: 1000;
  opacity: 0.95;
  pointer-events: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<svg class="ladybug" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="64" cy="76" r="40" fill="#000000"/>
  <path d="M24,76a40,40 0 0,0 80,0a40,40 0 0,0 -80,0" fill="#e53935" stroke="#000000" stroke-width="5"/>
  <line x1="64" y1="44" x2="64" y2="116" stroke="#000000" stroke-width="4"/>
  <circle cx="48" cy="76" r="6" fill="#000000"/>
  <circle cx="80" cy="76" r="6" fill="#000000"/>
  <circle cx="56" cy="94" r="6" fill="#000000"/>
  <circle cx="72" cy="94" r="6" fill="#000000"/>
  <circle cx="64" cy="40" r="16" fill="#000000"/>
  <circle cx="58" cy="38" r="6" fill="#ffffff"/>
  <circle cx="70" cy="38" r="6" fill="#ffffff"/>
  <path d="M54 26 C44 16, 34 14, 24 16" stroke="#000000" stroke-width="3" fill="none"/>
  <path d="M74 26 C84 16, 94 14, 104 16" stroke="#000000" stroke-width="3" fill="none"/>
</svg>
""", unsafe_allow_html=True)

st.title("Python Challenge Day 1")

with st.form("greeting_form"):
    name = st.text_input("Enter your name:")
    age = st.slider("Select your age:", 1, 100, 25)
    submit = st.form_submit_button("Submit")

if submit:
    st.success(f"Hello {name}! 🎉 You are {age} years young!")
