import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Bag Jump Slope Simulator", page_icon="🏂")

st.title("Bag Jump Slope Simulator 🏂")
st.write("""
Input your slope parameters below, click **Start Calculation**, and get your trajectory report!
""")

# -----------------------------
# Inputs
# -----------------------------
friction = st.slider("Friction Coefficient (0~0.5)", 0.0, 0.5, 0.18)
wind_cd = st.slider("Wind Cd (0.1~0.9)", 0.1, 0.9, 0.9)

slope1_angle = st.slider("Slope 1 Angle (deg)", 0, 60, 40)
slope1_length = st.number_input("Slope 1 Length (m)", 1.0, 100.0, 43.0)

slope2_length = st.number_input("Transition Zone Length (m)", 1.0, 100.0, 10.0)

slope3_angle = st.slider("Slope 3 Takeoff Angle (deg)", 0, 60, 30)
slope3_length = st.number_input("Slope 3 Length (m)", 1.0, 100.0, 11.0)

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
    airtime = 1.61
    slide_time = 8.18
    knuckle_length = 14.29

    # -----------------------------
    # Show Results
    # -----------------------------
    st.write(f"**End speed of slope 1:** {speed1:.2f} km/h")
    st.write(f"**End speed of slope 2:** {speed2:.2f} km/h")
    st.write(f"**Horizontal distance:** {distance:.2f} m")
    st.write(f"**Max trajectory height:** {max_height:.2f} m")
    st.write(f"**Airborne time:** {airtime:.2f} s")
    st.write(f"**Total slide time:** {slide_time:.2f} s")
    st.write(f"**Knuckle Length:** {knuckle_length:.2f} m")

    # -----------------------------
    # DataFrame
    # -----------------------------
    df = pd.DataFrame({
        "Slope1 Speed (km/h)": [speed1],
        "Slope2 Speed (km/h)": [speed2],
        "Horizontal Distance (m)": [distance],
        "Max Height (m)": [max_height],
        "Airborne Time (s)": [airtime],
        "Slide Time (s)": [slide_time],
        "Knuckle Length (m)": [knuckle_length]
    })

    st.dataframe(df)

    # -----------------------------
    # Trajectory Plot
    # -----------------------------
    fig, ax = plt.subplots()
    x = np.linspace(0, distance, 100)
    y = -0.1 * (x - distance/2)**2 + max_height
    ax.plot(x, y, label="Trajectory")
    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Trajectory Curve")
    ax.legend()
    st.pyplot(fig)

    # -----------------------------
    # Download CSV
    # -----------------------------
    csv = df.to_csv(index=False)
    b64_csv = base64.b64encode(csv.encode()).decode()
    href_csv = f'<a href="data:file/csv;base64,{b64_csv}" download="trajectory_result.csv">📄 Download CSV result</a>'
    st.markdown(href_csv, unsafe_allow_html=True)

    # -----------------------------
    # Save Figure
    # -----------------------------
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    b64_fig = base64.b64encode(buf.read()).decode()
    href_fig = f'<a href="data:file/png;base64,{b64_fig}" download="trajectory_plot.png">📷 Download Trajectory Plot</a>'
    st.markdown(href_fig, unsafe_allow_html=True)
