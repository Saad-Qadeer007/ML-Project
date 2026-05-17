import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from PIL import Image

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Hotel Energy Optimization",
    layout="wide",
    page_icon="⚡"
)

# ── Custom CSS – Top Navigation Bar ──────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit top bar */
    #MainMenu { visibility: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }

    /* ── Navbar container ── */
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 14px 36px;
        border-radius: 14px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    }

    .navbar-brand {
        font-size: 1.35rem;
        font-weight: 700;
        color: #f9d342;
        letter-spacing: 0.5px;
        text-shadow: 0 0 12px rgba(249,211,66,0.4);
    }

    .navbar-links {
        display: flex;
        gap: 10px;
    }

    .nav-btn {
        background: rgba(255,255,255,0.08);
        color: #e0e0e0;
        border: 1px solid rgba(255,255,255,0.15);
        padding: 8px 22px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.25s ease;
        text-decoration: none;
    }

    .nav-btn:hover {
        background: rgba(249,211,66,0.18);
        color: #f9d342;
        border-color: #f9d342;
        transform: translateY(-1px);
    }

    .nav-btn.active {
        background: linear-gradient(135deg, #f9d342, #f7971e);
        color: #1a1a2e;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 14px rgba(249,211,66,0.45);
    }

    /* ── Section headings ── */
    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f9d342;
        margin-bottom: 6px;
    }

    .section-sub {
        color: #aaa;
        font-size: 0.95rem;
        margin-bottom: 24px;
    }

    /* ── Hero card (Home) ── */
    .hero-card {
        background: linear-gradient(135deg, #0f0c29cc, #302b63cc);
        border: 1px solid rgba(249,211,66,0.25);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin-bottom: 28px;
    }

    .hero-emoji { font-size: 4rem; }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #f9d342;
        margin: 12px 0 8px;
        text-shadow: 0 0 20px rgba(249,211,66,0.3);
    }

    .hero-desc {
        color: #ccc;
        font-size: 1.05rem;
        max-width: 680px;
        margin: 0 auto;
        line-height: 1.7;
    }

    /* ── Feature cards (Home) ── */
    .feature-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 28px 24px;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(249,211,66,0.12);
        border-color: rgba(249,211,66,0.35);
    }

    .feature-icon { font-size: 2.2rem; margin-bottom: 10px; }

    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f9d342;
        margin-bottom: 6px;
    }

    .feature-desc { color: #bbb; font-size: 0.9rem; line-height: 1.6; }

    /* ── Metric cards ── */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 16px;
    }

    /* ── Divider ── */
    .custom-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin: 28px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Session State for active page ────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ── Navigation Bar ────────────────────────────────────────────────────────────
pages = ["Home", "Prediction Tool", "EDA Insights"]

def nav_button_class(name):
    return "nav-btn active" if st.session_state.page == name else "nav-btn"

# Render brand + buttons using columns
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([3, 1, 1, 1, 1])
with nav_col1:
    st.markdown("<div style='padding:8px 0; font-size:1.2rem; font-weight:700; color:#f9d342;'>⚡ HotelEnergy AI</div>", unsafe_allow_html=True)
with nav_col3:
    if st.button("🏠 Home", key="nav_home", use_container_width=True,
                 type="primary" if st.session_state.page == "Home" else "secondary"):
        st.session_state.page = "Home"
        st.rerun()
with nav_col4:
    if st.button("🔮 Prediction", key="nav_pred", use_container_width=True,
                 type="primary" if st.session_state.page == "Prediction Tool" else "secondary"):
        st.session_state.page = "Prediction Tool"
        st.rerun()
with nav_col5:
    if st.button("📊 EDA Insights", key="nav_eda", use_container_width=True,
                 type="primary" if st.session_state.page == "EDA Insights" else "secondary"):
        st.session_state.page = "EDA Insights"
        st.rerun()

st.markdown("<hr style='border:1px solid rgba(255,255,255,0.1); margin:4px 0 28px;'>", unsafe_allow_html=True)

# ── Load Models (cached) ──────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    demand_model = joblib.load('model/demand_model.pkl')
    energy_model  = joblib.load('model/energy_model.pkl')
    return demand_model, energy_model

try:
    demand_model, energy_model = load_models()
    models_loaded = True
except Exception as e:
    models_loaded = False
    model_error   = str(e)

# ── Month mapping ─────────────────────────────────────────────────────────────
month_map = {
    'January':1, 'February':2, 'March':3, 'April':4,
    'May':5, 'June':6, 'July':7, 'August':8,
    'September':9, 'October':10, 'November':11, 'December':12
}

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 – HOME
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "Home":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-emoji">⚡</div>
        <div class="hero-title">Smart Hotel Energy Optimization</div>
        <div class="hero-desc">
            An AI-powered platform that integrates hotel demand forecasting with
            building energy consumption models to help hospitality managers make
            smarter, data-driven energy decisions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏨</div>
            <div class="feature-title">Demand Forecasting</div>
            <div class="feature-desc">
                Predicts hotel occupancy percentage based on booking features
                like month, number of guests, and length of stay.
            </div>
        </div>""", unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏢</div>
            <div class="feature-title">Energy Modeling</div>
            <div class="feature-desc">
                Estimates base heating and cooling loads using the building's
                physical characteristics such as surface area and height.
            </div>
        </div>""", unsafe_allow_html=True)
    with f3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📉</div>
            <div class="feature-title">Optimized Consumption</div>
            <div class="feature-desc">
                Combines both predictions via an integration formula to compute
                occupancy-adjusted energy needs, reducing waste.
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    st.markdown("### 🗂️ How It Works")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.info("**Step 1 – Input**\n\nProvide hotel booking details and building physical parameters on the Prediction page.")
    with s2:
        st.success("**Step 2 – Predict**\n\nTwo ML models run simultaneously to estimate occupancy rate and base energy loads.")
    with s3:
        st.warning("**Step 3 – Optimize**\n\nThe integration formula combines both outputs into an optimized energy consumption figure.")

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    st.markdown("### 📦 Dataset Sources")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("""
        **Hotel Demand Dataset**
        - Source: `hotel_booking.csv`
        - Features: Month, Guests, Length of Stay
        - Target: Occupancy Percentage
        """)
    with d2:
        st.markdown("""
        **Building Energy Dataset**
        - Source: Power Laws Energy Consumption dataset
        - Features: Surface Area, Wall Area, Roof Area, Height
        - Targets: Heating Load, Cooling Load
        """)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 – PREDICTION TOOL
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Prediction Tool":
    st.markdown("<div class='section-title'>🔮 Prediction Tool</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Enter inputs below to predict hotel occupancy and optimized energy consumption.</div>", unsafe_allow_html=True)

    if not models_loaded:
        st.error(f"❌ Models could not be loaded. Please run `train_models.py` first.\n\n**Details:** {model_error}")
        st.stop()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("🏨 Hotel Demand Inputs")
        st.caption("Enter details to predict hotel occupancy.")
        month      = st.selectbox("Month of Stay", list(month_map.keys()))
        guests     = st.number_input("Number of Guests (Adults + Children + Babies)", min_value=1, max_value=20, value=2)
        stay_length = st.number_input("Total Length of Stay (Nights)", min_value=1, max_value=30, value=3)

    with col2:
        st.subheader("🏢 Building Energy Inputs")
        st.caption("Enter the building's physical characteristics.")
        surface_area = st.number_input("Surface Area (m²)", min_value=100.0, max_value=1000.0, value=514.5)
        wall_area    = st.number_input("Wall Area (m²)",    min_value=100.0, max_value=500.0,  value=294.0)
        roof_area    = st.number_input("Roof Area (m²)",    min_value=100.0, max_value=300.0,  value=110.25)
        height       = st.number_input("Building Height (m)", min_value=3.0, max_value=15.0, value=7.0)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    
    st.subheader("📺 Room Amenities & Appliances (Plug Load)")
    st.caption("Select the appliances available in each room to calculate dynamic plug loads.")
    c_app1, c_app2, c_app3 = st.columns(3)
    with c_app1:
        has_tv = st.checkbox("60-inch Smart TV (1.5 kWh/day)", value=True)
        has_fridge = st.checkbox("Mini-Fridge (2.0 kWh/day)", value=True)
    with c_app2:
        has_hairdryer = st.checkbox("High-Power Hairdryer (0.5 kWh/day)", value=False)
        has_kettle = st.checkbox("Electric Kettle (0.5 kWh/day)", value=True)
    with c_app3:
        has_jacuzzi = st.checkbox("In-Room Jacuzzi (5.0 kWh/day)", value=False)
        total_rooms = st.number_input("Total Rooms in Hotel", min_value=10, max_value=2000, value=100, step=10)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
    
    st.subheader("💰 Financial & Optimization Settings")
    st.caption("Set the local energy unit price and baseline maintenance energy.")
    c_fin1, c_fin2 = st.columns(2)
    with c_fin1:
        unit_price = st.number_input("Energy Unit Price ($/kWh)", min_value=0.01, max_value=10.00, value=0.15, step=0.01)
    with c_fin2:
        fixed_maintenance = st.number_input("Fixed Maintenance Energy (kWh/m²)", min_value=0.0, max_value=50.0, value=5.0, step=0.5)

    st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

    if st.button("⚡ Run Predictive Analysis", type="primary", use_container_width=True):
        with st.spinner("Analyzing data..."):
            # 1. Demand Prediction
            month_num    = month_map[month]
            demand_input = pd.DataFrame({
                'Month_num':       [month_num],
                'Number_of_guests':[guests],
                'Length_of_stay':  [stay_length]
            })
            occupancy_pct = demand_model.predict(demand_input)[0]
            occupancy_pct = max(0.01, min(1.0, occupancy_pct))

            # 2. Energy Prediction
            energy_input = pd.DataFrame({
                'Surface_Area':   [surface_area],
                'Wall_Area':      [wall_area],
                'Roof_Area':      [roof_area],
                'Building_Height':[height]
            })
            base_energy   = energy_model.predict(energy_input)[0]
            base_heating  = base_energy[0]
            base_cooling  = base_energy[1]

            # 3. Integration Formula (HVAC)
            final_heating = (base_heating * occupancy_pct) + (fixed_maintenance / 2)
            final_cooling = (base_cooling * occupancy_pct) + (fixed_maintenance / 2)

            # 4. Appliance / Plug Load Calculation
            daily_appliance_kwh = 0.0
            if has_tv: daily_appliance_kwh += 1.5
            if has_fridge: daily_appliance_kwh += 2.0
            if has_hairdryer: daily_appliance_kwh += 0.5
            if has_kettle: daily_appliance_kwh += 0.5
            if has_jacuzzi: daily_appliance_kwh += 5.0
            
            active_rooms = int(total_rooms * occupancy_pct)
            
            # Assume Baseline operates as if hotel is 100% full (worst case)
            base_appliance_load = daily_appliance_kwh * total_rooms
            optimized_appliance_load = daily_appliance_kwh * active_rooms

            # 5. Cost Calculation (converting everything to absolute kWh)
            absolute_base_hvac = (base_heating + base_cooling) * surface_area
            absolute_final_hvac = (final_heating + final_cooling) * surface_area
            
            total_base_kwh = absolute_base_hvac + base_appliance_load
            total_final_kwh = absolute_final_hvac + optimized_appliance_load
            
            base_cost = total_base_kwh * unit_price
            final_cost = total_final_kwh * unit_price
            savings = base_cost - final_cost

        st.success("✅ Analysis complete!")
        st.markdown("### 📈 HVAC Optimization Results")

        c1, c2, c3 = st.columns(3)
        c1.metric("Predicted Occupancy Level",    f"{occupancy_pct*100:.2f} %")
        c2.metric("Base Heating Load",            f"{base_heating:.2f} kWh/m²")
        c3.metric("Adjusted Heating (Optimized)", f"{final_heating:.2f} kWh/m²",
                  delta=f"{(final_heating - base_heating):.2f} kWh/m²", delta_color="inverse")

        c4, c5, c6 = st.columns(3)
        c4.metric("Active Rooms (Estimated)", f"{active_rooms} / {total_rooms}")
        c5.metric("Base Cooling Load",          f"{base_cooling:.2f} kWh/m²")
        c6.metric("Adjusted Cooling (Optimized)", f"{final_cooling:.2f} kWh/m²",
                  delta=f"{(final_cooling - base_cooling):.2f} kWh/m²", delta_color="inverse")

        st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
        st.markdown("### 🔌 Appliance & Plug Load Impact")
        a1, a2, a3 = st.columns(3)
        a1.metric("Appliance Energy per Room", f"{daily_appliance_kwh:.1f} kWh/day")
        a2.metric("Base Appliance Load (100% Full)", f"{base_appliance_load:.1f} kWh/day")
        a3.metric("Optimized Appliance Load", f"{optimized_appliance_load:.1f} kWh/day", delta=f"-{(base_appliance_load - optimized_appliance_load):.1f} kWh/day", delta_color="inverse")

        st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
        st.markdown("### 🧮 Final Integration Formula")
        st.latex(r"\text{Total Energy} = \text{Optimized HVAC (Area)} + \text{Active Appliance Load}")
        st.info(f"Total Base Energy (HVAC + Appliances) would be **{total_base_kwh:.1f} kWh**. Optimized Total is **{total_final_kwh:.1f} kWh**.")

        st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
        st.markdown("### 💰 Financial Impact")
        f1, f2, f3 = st.columns(3)
        f1.metric("Base Total Cost", f"${base_cost:.2f}")
        f2.metric("Optimized Total Cost", f"${final_cost:.2f}", delta=f"-${savings:.2f}", delta_color="normal")
        f3.metric("Total Cost Savings", f"${savings:.2f}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – EDA INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "EDA Insights":
    st.markdown("<div class='section-title'>📊 Exploratory Data Analysis Insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Historical patterns discovered during the model training phase.</div>", unsafe_allow_html=True)

    images = {
        "Monthly Booking Trends":       "images/monthly_booking_trends.png",
        "Distribution of Guests":        "images/guest_distribution.png",
        "Heating Load vs Input Features":"images/heating_load_features.png",
        "Energy Efficiency Correlation": "images/energy_correlation.png",
    }

    available = {k: v for k, v in images.items() if os.path.exists(v)}
    missing   = {k: v for k, v in images.items() if not os.path.exists(v)}

    if not available:
        st.warning("⚠️ No EDA images found. Please run `train_models.py` to generate them in the `images/` directory.")
    else:
        # Hotel demand section
        st.markdown("#### 🏨 Hotel Demand Analysis")
        hotel_imgs = {k: v for k, v in available.items()
                      if k in ["Monthly Booking Trends", "Distribution of Guests"]}
        if hotel_imgs:
            cols = st.columns(len(hotel_imgs))
            for col, (caption, path) in zip(cols, hotel_imgs.items()):
                with col:
                    img = Image.open(path)
                    st.image(img, caption=caption, use_column_width=True)

        st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

        # Building energy section
        st.markdown("#### 🏢 Building Energy Analysis")
        bldg_imgs = {k: v for k, v in available.items()
                     if k in ["Heating Load vs Input Features", "Energy Efficiency Correlation"]}
        if bldg_imgs:
            cols = st.columns(len(bldg_imgs))
            for col, (caption, path) in zip(cols, bldg_imgs.items()):
                with col:
                    img = Image.open(path)
                    st.image(img, caption=caption, use_column_width=True)

    if missing:
        st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
        with st.expander("⚠️ Missing EDA Images"):
            for caption, path in missing.items():
                st.write(f"- **{caption}** → `{path}`")
            st.info("Run `python train_models.py` to regenerate all EDA plots.")
