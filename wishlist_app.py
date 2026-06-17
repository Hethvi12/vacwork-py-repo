import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

EXCEL_FILE = Path(__file__).parent / "wishlist.xlsx"

st.set_page_config(page_title="Electronic Components Wishlist", layout="centered")

st.markdown("""
<style>
    /* Pastel blue background */
    .stApp {
        background-color: #ddeeff;
    }

    /* Card container */
    .block-container {
        background-color: #eaf4ff;
        border-radius: 16px;
        padding: 2.5rem 3rem !important;
        max-width: 760px;
        margin: 2rem auto;
        box-shadow: 0 4px 20px rgba(100, 160, 220, 0.25);
    }

    /* Labels */
    label, .stTextInput label, .stNumberInput label, .stTextArea label {
        font-size: 1.08rem !important;
        font-weight: 600 !important;
        color: #2a4a6b !important;
        margin-bottom: 5px !important;
    }

    /* Input fields - generous space */
    .stTextInput input, .stNumberInput input {
        background-color: #ffffff !important;
        border: 1.5px solid #a8c8e8 !important;
        border-radius: 8px !important;
        font-size: 1.05rem !important;
        padding: 12px 16px !important;
        color: #1a3a5c !important;
        min-height: 48px !important;
    }
    .stTextArea textarea {
        background-color: #ffffff !important;
        border: 1.5px solid #a8c8e8 !important;
        border-radius: 8px !important;
        font-size: 1.05rem !important;
        padding: 12px 16px !important;
        color: #1a3a5c !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: #4a90d9 !important;
        box-shadow: 0 0 0 3px rgba(74, 144, 217, 0.2) !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #4a90d9 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 11px 30px !important;
        font-size: 1.02rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: background-color 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #357abd !important;
    }

    h1 {
        color: #1a3a5c !important;
        font-size: 2.1rem !important;
        margin-bottom: 0.2rem !important;
    }
    p.subtitle {
        color: #4a7aaa;
        font-size: 1.02rem;
        margin-bottom: 1.8rem;
    }

    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #a8c8e8;
    }

    hr {
        border-color: #b8d4ee;
        margin: 1.6rem 0;
    }

    .success-msg {
        background-color: #d4edda;
        border: 1px solid #a8d5b5;
        border-radius: 8px;
        padding: 11px 18px;
        color: #1e5c34;
        font-weight: 600;
        margin-top: 0.6rem;
    }
</style>
""", unsafe_allow_html=True)


def load_data() -> pd.DataFrame:
    if EXCEL_FILE.exists():
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame(columns=["#", "Component", "Model", "Specifications", "Quantity", "Date Added"])


def save_row(component, model, specs, qty):
    df = load_data()
    new_row = {
        "#": len(df) + 1,
        "Component": component,
        "Model": model,
        "Specifications": specs,
        "Quantity": qty,
        "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)


# --- State init ---
for key, default in [
    ("step", 0),
    ("component", ""),
    ("model", ""),
    ("specs", ""),
    ("qty", 1),
    ("saved", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


st.title("Electronic Components Wishlist")
st.markdown('<p class="subtitle">Fill in each field and press Enter to move on to the next one.</p>', unsafe_allow_html=True)

step = st.session_state.step

# ── Step 0: Component ──────────────────────────────────────────────
component_val = st.text_input(
    "Component",
    value=st.session_state.component,
    placeholder="e.g. Resistor, Capacitor, Microcontroller…",
    key="input_component",
    disabled=(step > 0),
)
if step == 0 and component_val.strip():
    # Enter key fills this value and triggers a rerun -> advance automatically
    st.session_state.component = component_val
    st.session_state.step = 1
    st.rerun()

if step == 0 and st.button("Next →", key="btn0"):
    if component_val.strip():
        st.session_state.component = component_val
        st.session_state.step = 1
        st.rerun()
    else:
        st.warning("Please enter a component name.")

# ── Step 1: Model ──────────────────────────────────────────────────
if step >= 1:
    model_val = st.text_input(
        "Model",
        value=st.session_state.model,
        placeholder="e.g. NE555, ATmega328P, LM7805…",
        key="input_model",
        disabled=(step > 1),
    )
    if step == 1 and model_val.strip():
        st.session_state.model = model_val
        st.session_state.step = 2
        st.rerun()

    if step == 1 and st.button("Next →", key="btn1"):
        if model_val.strip():
            st.session_state.model = model_val
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Please enter a model.")

# ── Step 2: Specifications ─────────────────────────────────────────
if step >= 2:
    specs_val = st.text_area(
        "Specifications",
        value=st.session_state.specs,
        placeholder="e.g. 10kΩ ±1% 0.25W, 100µF 25V electrolytic…",
        height=120,
        key="input_specs",
        disabled=(step > 2),
    )
    if step == 2 and specs_val:
        st.session_state.specs = specs_val

    if step == 2 and st.button("Next →", key="btn2"):
        if st.session_state.specs.strip():
            st.session_state.step = 3
            st.rerun()
        else:
            st.warning("Please enter specifications.")

# ── Step 3: Quantity ───────────────────────────────────────────────
if step >= 3:
    qty_val = st.number_input(
        "Quantity",
        min_value=1,
        max_value=100000,
        value=st.session_state.qty,
        step=1,
        key="input_qty",
    )
    st.session_state.qty = int(qty_val)

    st.markdown("")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Add to Wishlist", key="btn_save"):
            save_row(
                st.session_state.component,
                st.session_state.model,
                st.session_state.specs,
                st.session_state.qty,
            )
            st.session_state.saved = True
            st.session_state.step = 0
            st.session_state.component = ""
            st.session_state.model = ""
            st.session_state.specs = ""
            st.session_state.qty = 1
            st.rerun()
    with col2:
        if st.button("Start Over", key="btn_reset"):
            st.session_state.step = 0
            st.session_state.component = ""
            st.session_state.model = ""
            st.session_state.specs = ""
            st.session_state.qty = 1
            st.rerun()

if st.session_state.saved:
    st.markdown('<div class="success-msg">✓ Component added and saved to Excel!</div>', unsafe_allow_html=True)
    st.session_state.saved = False

# ── Wishlist table ─────────────────────────────────────────────────
df = load_data()
if not df.empty:
    st.markdown("---")
    st.subheader(f"Wishlist ({len(df)} item{'s' if len(df) != 1 else ''})")
    st.dataframe(df, use_container_width=True, hide_index=True)

    with open(EXCEL_FILE, "rb") as f:
        st.download_button(
            label="Download Wishlist (.xlsx)",
            data=f,
            file_name="wishlist.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
