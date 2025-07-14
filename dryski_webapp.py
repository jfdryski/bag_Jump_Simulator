import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# -----------------------------
# Streamlit basic settings
# -----------------------------
st.set_page_config(page_title="Bag Jump Simulator", page_icon="🏂")

st.title("Bag Jump Slope Simulator 🏂")
st.write("""
Input your slope parameters below, click **Start Calculation**, and get your trajectory report!
""")

# -----------------------------
# User Inputs
# -----------------------------
friction = st.slider("Friction Coefficient (0~0.5)", 0.0, 0.5, 0.18)
wind_cd = st.slider("Wind Cd (0.1~0.9)", 0.1, 0.9, 0.9)
slope_angle = st.slider("Slope Angle 1 (deg)", 0, 60, 40)
slope_length = st.number_input("Slope Length 1 (m)", 1.0, 100.0, 43.0)

# -----------------------------
# Calculate Button
# -----------------------------
if st.button("Start Calculation"):
    st.success("Calculation Done!")

    # -----------------------------
    # Dummy Example Calculation
    # -----------------------------
    speed1 = 74.3
    speed2 = 56.8
    distance = 21.99
    max_height = 3.17

    # -----------------------------
    # Show Results
    # -----------------------------
    st.write(f"**End speed of slope 1:** {speed1} km/h")
    st.write(f"**End speed of slope 2:** {speed2} km/h")
    st.write(f"**Horizontal distance:** {distance} m")
    st.write(f"**Max height:** {max_height} m")

    # -----------------------------
    # DataFrame
    # -----------------------------
    df = pd.DataFrame({
        "Slope1 Speed": [speed1],
        "Slope2 Speed": [speed2],
        "Horizontal Distance": [distance],
        "Max Height": [max_height]
    })

    st.dataframe(df)

    # -----------------------------
    # Plot Trajectory
    # -----------------------------
    fig, ax = plt.subplots()
    x = np.linspace(0, distance, 100)
    y = -0.1 * (x - distance/2)**2 + max_height
    ax.plot(x, y)
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Trajectory Curve")
    st.pyplot(fig)

    # -----------------------------
    # Download Result
    # -----------------------------
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="result.csv">📄 Download CSV result</a>'
    st.markdown(href, unsafe_allow_html=True)
