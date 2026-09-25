import random
from datetime import datetime

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="A.G.I.L.E. Simulation",
    page_icon="🐟",
    layout="wide"
)

st.title("🐟 A.G.I.L.E. — AI Hatchery Risk Simulation")
st.caption("Aqua Genesis for Intelligent Lifecycle & Early Prediction")

st.info(
    "Simulation mode: sensor and behaviour values are generated virtually. "
    "Later, these inputs can be replaced with real sensors and camera/AI data."
)


# ---------------- RISK CALCULATION ----------------

def calculate_risk(
    temperature,
    ph,
    dissolved_oxygen,
    turbidity,
    ammonia,
    activity,
    feeding,
    growth,
    molting
):

    risk = 0

    # Water quality
    if temperature < 26 or temperature > 30:
        risk += 15

    if ph < 7.0 or ph > 8.5:
        risk += 15

    if dissolved_oxygen < 5:
        risk += 20

    if turbidity > 25:
        risk += 10

    if ammonia > 0.5:
        risk += 20

    # Behaviour
    if activity < 50:
        risk += 10

    if feeding < 50:
        risk += 5

    if growth < 50:
        risk += 5

    if molting < 50:
        risk += 5

    risk = min(risk, 100)

    if risk < 30:
        status = "LOW"
        recommendation = "Continue normal monitoring."

    elif risk < 60:
        status = "MEDIUM"
        recommendation = (
            "Inspect water quality and observe feeding and activity."
        )

    else:
        status = "HIGH"
        recommendation = (
            "Immediate inspection recommended. "
            "Check water quality and larval behaviour."
        )

    return risk, status, recommendation


# ---------------- SIDEBAR ----------------

st.sidebar.header("Simulation Controls")

mode = st.sidebar.radio(
    "Select Input Mode",
    ["Normal", "Custom", "Random Event"]
)


# ---------------- INPUT VALUES ----------------

if mode == "Normal":

    temperature = 28.0
    ph = 7.8
    dissolved_oxygen = 6.2
    turbidity = 12
    ammonia = 0.20

    activity = 82
    feeding = 75
    growth = 80
    molting = 70


elif mode == "Random Event":

    temperature = random.uniform(24, 32)
    ph = random.uniform(6.5, 9.0)
    dissolved_oxygen = random.uniform(3, 7)
    turbidity = random.uniform(5, 45)
    ammonia = random.uniform(0.1, 1.0)

    activity = random.randint(20, 90)
    feeding = random.randint(20, 90)
    growth = random.randint(30, 90)
    molting = random.randint(30, 90)


else:

    temperature = st.sidebar.slider(
        "Temperature (°C)",
        20.0, 35.0, 28.0
    )

    ph = st.sidebar.slider(
        "pH",
        5.0, 10.0, 7.8
    )

    dissolved_oxygen = st.sidebar.slider(
        "Dissolved Oxygen (mg/L)",
        1.0, 10.0, 6.2
    )

    turbidity = st.sidebar.slider(
        "Turbidity (NTU)",
        0.0, 60.0, 12.0
    )

    ammonia = st.sidebar.slider(
        "Ammonia (mg/L)",
        0.0, 2.0, 0.2
    )

    activity = st.sidebar.slider(
        "Activity (%)",
        0, 100, 82
    )

    feeding = st.sidebar.slider(
        "Feeding Response (%)",
        0, 100, 75
    )

    growth = st.sidebar.slider(
        "Growth Indicator (%)",
        0, 100, 80
    )

    molting = st.sidebar.slider(
        "Molting Indicator (%)",
        0, 100, 70
    )


# ---------------- CALCULATE RISK ----------------

risk, status, recommendation = calculate_risk(
    temperature,
    ph,
    dissolved_oxygen,
    turbidity,
    ammonia,
    activity,
    feeding,
    growth,
    molting
)


# ---------------- WATER QUALITY ----------------

st.subheader("🌊 Water Quality")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Temperature",
    f"{temperature:.1f} °C"
)

c2.metric(
    "pH",
    f"{ph:.1f}"
)

c3.metric(
    "Dissolved O₂",
    f"{dissolved_oxygen:.1f} mg/L"
)

c4.metric(
    "Turbidity",
    f"{turbidity:.0f} NTU"
)

c5.metric(
    "Ammonia",
    f"{ammonia:.2f} mg/L"
)


st.divider()


# ---------------- AI RISK ----------------

left, right = st.columns(2)


with left:

    st.subheader("🤖 AI Risk Assessment")

    st.metric(
        "Risk Score",
        f"{risk}/100"
    )

    if status == "LOW":

        st.success("🟢 LOW RISK")

    elif status == "MEDIUM":

        st.warning("🟡 MEDIUM RISK")

    else:

        st.error("🔴 HIGH RISK")

    st.write(
        "**Recommendation:**",
        recommendation
    )


# ---------------- BEHAVIOUR ----------------

with right:

    st.subheader("🐟 Larvae Behaviour")

    behaviour_data = pd.DataFrame(
        {
            "Indicator": [
                "Activity",
                "Feeding",
                "Growth",
                "Molting"
            ],

            "Score": [
                activity,
                feeding,
                growth,
                molting
            ]
        }
    )

    st.bar_chart(
        behaviour_data.set_index("Indicator")
    )


st.divider()


# ---------------- HISTORY ----------------

st.subheader("📈 Simulated Sensor History")

if "history" not in st.session_state:

    st.session_state.history = []


if st.button("➕ Add Current Reading"):

    st.session_state.history.append(
        {
            "Time": datetime.now().strftime("%H:%M:%S"),

            "Temperature": temperature,

            "pH": ph,

            "DO": dissolved_oxygen,

            "Turbidity": turbidity,

            "Ammonia": ammonia,

            "Risk": risk
        }
    )


if st.session_state.history:

    history = pd.DataFrame(
        st.session_state.history
    )

    st.line_chart(
        history.set_index("Time")[
            [
                "Temperature",
                "pH",
                "DO",
                "Risk"
            ]
        ]
    )

    st.dataframe(
        history,
        use_container_width=True
    )

else:

    st.write(
        "Click **Add Current Reading** to create simulated history."
    )


st.divider()

st.caption(
    "A.G.I.L.E. prototype simulation — "
    "simulated data → risk analysis → dashboard."
)