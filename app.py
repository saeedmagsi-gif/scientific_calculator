# Scientific Calculator — Casio fx-991EX style (Streamlit)
# Deploy to Hugging Face Spaces or Streamlit Cloud

import math
import streamlit as st
from typing import Tuple

# Page config
st.set_page_config(
    page_title="Casio Scientific Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Safe math environment ---
SAFE_MATH = {
    'pi': math.pi,
    'e': math.e,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,
    'asinh': math.asinh,
    'acosh': math.acosh,
    'atanh': math.atanh,
    'log': lambda x, base=math.e: math.log(x, base) if base != math.e else math.log(x),
    'ln': math.log,
    'log10': math.log10,
    'sqrt': math.sqrt,
    'abs': abs,
    'round': round,
    'floor': math.floor,
    'ceil': math.ceil,
    'exp': math.exp,
    'pow': pow,
    'factorial': math.factorial,
}

if hasattr(math, 'comb'):
    SAFE_MATH['comb'] = math.comb
if hasattr(math, 'perm'):
    SAFE_MATH['perm'] = math.perm

EVAL_GLOBALS = {k: v for k, v in SAFE_MATH.items()}
SAFE_GLOBALS = {"__builtins__": None}

# --- Initialize session state ---
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'result' not in st.session_state:
    st.session_state.result = '0'
if 'shift_mode' not in st.session_state:
    st.session_state.shift_mode = False
if 'angle_unit' not in st.session_state:
    st.session_state.angle_unit = 'deg'
if 'memory' not in st.session_state:
    st.session_state.memory = ''
if 'last_result' not in st.session_state:
    st.session_state.last_result = '0'

# --- Evaluator ---
def safe_eval(expr: str, angle_unit: str = 'deg') -> Tuple[str, bool]:
    if expr.strip() == '':
        return ("", False)
    expr = expr.replace('^', '**')
    local_ns = dict(EVAL_GLOBALS)

    # degree-aware wrappers
    if angle_unit == 'deg':
        local_ns.update({
            'sind': lambda x: math.sin(math.radians(x)),
            'cosd': lambda x: math.cos(math.radians(x)),
            'tand': lambda x: math.tan(math.radians(x)),
            'asind': lambda x: math.degrees(math.asin(x)),
            'acosd': lambda x: math.degrees(math.acos(x)),
            'atand': lambda x: math.degrees(math.atan(x)),
        })
        for func in ('sin', 'cos', 'tan', 'asin', 'acos', 'atan'):
            expr = expr.replace(f"{func}(", f"{func}d(")

    try:
        result = eval(expr, SAFE_GLOBALS, local_ns)
        if isinstance(result, float):
            result_str = ('{:.12g}'.format(result))
        else:
            result_str = str(result)
        return (result_str, False)
    except Exception as e:
        return (f"Error: {e}", True)

# --- Button handlers ---
def append_to_expression(token: str):
    if token == 'ans':
        st.session_state.expression += st.session_state.last_result
    else:
        st.session_state.expression += token
    if st.session_state.shift_mode:
        st.session_state.shift_mode = False

def clear_expression():
    st.session_state.expression = ''
    st.session_state.result = '0'

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def calculate():
    res, err = safe_eval(st.session_state.expression, st.session_state.angle_unit)
    st.session_state.result = res
    st.session_state.last_result = res

def toggle_shift():
    st.session_state.shift_mode = not st.session_state.shift_mode

def memory_store():
    try:
        val = float(st.session_state.result)
        st.session_state.memory = str(val)
    except:
        pass

def memory_recall():
    st.session_state.expression += st.session_state.memory

def memory_clear():
    st.session_state.memory = ''

# --- Custom CSS - Premium Gradio-like design ---
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main background - dark theme */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%) !important;
    }
    
    /* Calculator container - premium look */
    .main .block-container {
        max-width: 880px;
        padding: 24px;
        background: linear-gradient(145deg, #2a2a2a 0%, #252525 100%);
        border-radius: 16px;
        box-shadow: 
            0 20px 60px rgba(0,0,0,0.8),
            0 0 0 1px rgba(255,255,255,0.05);
        margin-top: 2rem;
    }
    
    /* Title styling */
    h3 {
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Display box - sleek black screen */
    .display-box {
        background: linear-gradient(180deg, #0a0a0a 0%, #0f0f0f 100%);
        padding: 16px 18px;
        border-radius: 10px;
        margin-bottom: 16px;
        min-height: 110px;
        box-shadow: 
            inset 0 4px 12px rgba(0,0,0,0.6),
            inset 0 1px 3px rgba(0,0,0,0.8),
            0 1px 0 rgba(255,255,255,0.03);
        border: 1px solid #1a1a1a;
    }
    
    /* Input display - subtle text */
    .input-display {
        color: #8a8a8a;
        font-size: 15px;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'Consolas', monospace;
        margin-bottom: 10px;
        padding: 6px 4px;
        min-height: 32px;
        font-weight: 400;
        letter-spacing: 0.3px;
        word-wrap: break-word;
        word-break: break-all;
    }
    
    /* Output display - bright green result */
    .output-display {
        color: #00ff88;
        font-size: 32px;
        font-weight: 700;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', 'Consolas', monospace;
        text-align: right;
        padding: 6px 4px;
        border-top: 1px solid #1f1f1f;
        padding-top: 12px;
        min-height: 44px;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
    }
    
    /* All buttons - base style */
    .stButton > button {
        width: 100%;
        height: 52px;
        background: linear-gradient(145deg, #3d3d3d 0%, #353535 100%) !important;
        color: #ffffff !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        cursor: pointer;
        font-size: 15px !important;
        transition: all 0.15s ease;
        box-shadow: 
            0 2px 5px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.08);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        background: linear-gradient(145deg, #454545 0%, #3d3d3d 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 1px 3px rgba(0,0,0,0.4);
    }
    
    /* SHIFT button - blue when active */
    .stButton > button[kind="primary"] {
        background: linear-gradient(145deg, #2563eb 0%, #1d4ed8 100%) !important;
        border-color: #1e40af !important;
        box-shadow: 
            0 2px 5px rgba(37, 99, 235, 0.4),
            inset 0 1px 0 rgba(255,255,255,0.2);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(145deg, #3b82f6 0%, #2563eb 100%) !important;
    }
    
    /* Dropdown styling */
    .stSelectbox {
        margin-bottom: 0;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #3d3d3d 0%, #353535 100%) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #2a2a2a !important;
        height: 52px;
        display: flex;
        align-items: center;
    }
    
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 500 !important;
        margin-bottom: 4px !important;
    }
    
    /* Remove padding between buttons */
    .stButton {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    div[data-testid="column"] {
        padding: 3px !important;
    }
    
    /* Horizontal line */
    hr {
        margin: 16px 0;
        border: none;
        border-top: 1px solid #333;
        opacity: 0.5;
    }
    
    /* Footer text */
    .footer-text {
        color: #666;
        font-size: 12px;
        text-align: center;
        margin-top: 16px;
        font-weight: 400;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 16px;
        }
        
        .stButton > button {
            height: 46px;
            font-size: 14px !important;
        }
        
        .output-display {
            font-size: 26px;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Main UI ---
st.markdown("### Scientific Calculator — Casio fx-991EX style")

# Display
st.markdown('<div class="display-box">', unsafe_allow_html=True)
input_text = st.session_state.expression if st.session_state.expression else "Enter expression..."
st.markdown(f'<div class="input-display">{input_text}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="output-display">{st.session_state.result}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Top controls
col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
with col1:
    new_angle = st.selectbox('Angle Unit', ['deg', 'rad'], 
                             index=0 if st.session_state.angle_unit == 'deg' else 1, 
                             key='angle_select')
    if new_angle != st.session_state.angle_unit:
        st.session_state.angle_unit = new_angle
        st.rerun()

with col2:
    if st.button('SHIFT', type='primary' if st.session_state.shift_mode else 'secondary', key='shift_btn'):
        toggle_shift()
        st.rerun()

with col3:
    if st.button('AC', key='ac_btn'):
        clear_expression()
        st.rerun()

with col4:
    if st.button('⌫', key='back_btn'):
        backspace()
        st.rerun()

with col5:
    if st.button('=', key='equals_btn'):
        calculate()
        st.rerun()

# Button definitions
normal_labels = [
    'x²','√','ln','log','(',')',
    'sin','cos','tan','sin⁻¹','cos⁻¹','tan⁻¹',
    '7','8','9','÷','π','e',
    '4','5','6','×','%','EE',
    '1','2','3','−','Ans','EXP',
    '0','00','.','+','nPr','nCr'
]

shift_labels = [
    'x³','^','10^x','10^','(',')',
    'sinh','cosh','tanh','sinh⁻¹','cosh⁻¹','tanh⁻¹',
    '7','8','9','÷','π','e',
    '4','5','6','×','%','EE',
    '1','2','3','−','Ans','EXP',
    '0','00','.','+','P','C'
]

normal_tokens = [
    '**2', 'sqrt(', 'ln(', 'log10(', '(',')',
    'sin(', 'cos(', 'tan(', 'asin(', 'acos(', 'atan(',
    '7','8','9','/','pi','e',
    '4','5','6','*','%','E',
    '1','2','3','-','ans','E',
    '0','00','.','+','perm(', 'comb('
]

shift_tokens = [
    '**3', '**', '10**', '10**', '(',')',
    'sinh(', 'cosh(', 'tanh(', 'asinh(', 'acosh(', 'atanh(',
    '7','8','9','/','pi','e',
    '4','5','6','*','%','E',
    '1','2','3','-','ans','E',
    '0','00','.','+','perm(', 'comb('
]

# Keypad (6 columns, 6 rows)
for row in range(6):
    cols = st.columns(6)
    for col_idx in range(6):
        btn_idx = row * 6 + col_idx
        if btn_idx < len(normal_labels):
            label = shift_labels[btn_idx] if st.session_state.shift_mode else normal_labels[btn_idx]
            token = shift_tokens[btn_idx] if st.session_state.shift_mode else normal_tokens[btn_idx]
            
            with cols[col_idx]:
                if st.button(label, key=f'btn_{btn_idx}'):
                    append_to_expression(token)
                    st.rerun()

st.markdown("---")

# Memory buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('M+ (Store)', key='m_store'):
        memory_store()
        st.rerun()
with col2:
    if st.button('MR (Recall)', key='m_recall'):
        memory_recall()
        st.rerun()
with col3:
    if st.button('MC (Clear)', key='m_clear'):
        memory_clear()
        st.rerun()

st.markdown('<p class="footer-text">Casio-style scientific calculator with functional SHIFT button</p>', unsafe_allow_html=True)
