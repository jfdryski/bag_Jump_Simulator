import streamlit as st
import math
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False
import pandas as pd
import io

st.set_page_config(page_title="JFdryski 尖锋旱雪 麦秆气垫跳台参数生成器", page_icon=":ski:", layout="centered")

st.image("JFdryski_logo.png", width=200)  # 请把LOGO文件放到同一目录
st.title("🎿 JFdryski 气垫跳台参数生成器")

st.markdown("输入滑道参数，一键计算并下载报告！")

# 用户输入
mu = st.slider("摩擦系数 (0~0.5)", 0.0, 0.5, 0.18)
Cd = st.slider("风阻值 Cd (0.1~0.9)", 0.1, 0.9, 0.9)
theta1_deg = st.slider("第一段下滑坡角度 (°)", 10, 60, 40)
L1 = st.number_input("第一段下滑坡长度 (m)", 5, 100, 43)
theta2_deg = st.slider("第二段过度区角度 (°)", 0, 10, 0)
L2 = st.number_input("第二段过度区长度 (m)", 0, 20, 10)
theta3_deg = st.slider("第三段上坡角度 (°)", 0, 60, 30)
L3 = st.number_input("第三段上坡长度 (m)", 1, 20, 11)

if st.button("开始计算"):
    theta1 = math.radians(theta1_deg)
    theta2 = math.radians(theta2_deg)
    theta3 = math.radians(theta3_deg)
    g = 9.81

    # 计算
    h1 = L1 * math.sin(theta1)
    Wf1 = mu * g * math.cos(theta1) * L1
    v1 = math.sqrt(2 * g * h1 - 2 * Wf1)
    v1_kmh = v1 * 3.6

    Wf2 = mu * g * math.cos(theta2) * L2
    v2 = math.sqrt(max(v1**2 - 2 * Wf2, 0))

    h3 = L3 * math.sin(theta3)
    Wf3 = mu * g * math.cos(theta3) * L3
    v3 = math.sqrt(max(v2**2 - 2 * g * h3 - 2 * Wf3, 0))
    v3_kmh = v3 * 3.6

    vx = v3 * math.cos(theta3)
    vy = v3 * math.sin(theta3)
    t_flight = 2 * vy / g if vy > 0 else 0
    x_range = vx * t_flight if vy > 0 else 0
    h_max = vy**2 / (2 * g) if vy > 0 else 0
    knuckle = x_range * 0.65

    t1 = L1 / (v1 / 2) if v1 > 0 else 0
    t2 = L2 / (v2 / 2) if v2 > 0 else 0
    t3 = L3 / (v3 / 2) if v3 > 0 else 0
    t_total = t1 + t2 + t3 + t_flight

    st.success(f"""
    ① 第一段结束时速度：{v1_kmh:.2f} km/h  
    ② 第三段结束时速度：{v3_kmh:.2f} km/h  
    ③ 抛物线水平距离：{x_range:.2f} m  
    ④ 抛物线最大高度：{h_max:.2f} m  
    ⑤ 空中飞行时间：{t_flight:.2f} s  
    ⑥ 全程滑行时间：{t_total:.2f} s  
    ⑦ 前台距 Knuckle 长度：{knuckle:.2f} m  
    """)

    # Excel 下载
    df = pd.DataFrame({
        "参数": ["第一段结束时速度 km/h", "第三段结束时速度 km/h",
                "抛物线水平距离 m", "抛物线最大高度 m",
                "空中飞行时间 s", "全程滑行时间 s", "前台距 Knuckle m"],
        "数值": [v1_kmh, v3_kmh, x_range, h_max, t_flight, t_total, knuckle]
    })
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 下载计算结果 CSV", csv, "dryski_result.csv")

    # 轨迹示意图
    fig, ax = plt.subplots()
    ax.plot([0, L1 * math.cos(theta1)], [0, -L1 * math.sin(theta1)], label="In run")
    ax.plot([L1 * math.cos(theta1), L1 * math.cos(theta1) + L2], [-L1 * math.sin(theta1), -L1 * math.sin(theta1)], label="Buffer")
    ax.plot([L1 * math.cos(theta1) + L2, L1 * math.cos(theta1) + L2 + L3 * math.cos(theta3)],
            [-L1 * math.sin(theta1), -L1 * math.sin(theta1) + L3 * math.sin(theta3)], label="Kicker")
    if t_flight > 0:
        t = [i * t_flight / 50 for i in range(51)]
        x = [vx * ti for ti in t]
        y = [vy * ti - 0.5 * g * ti ** 2 for ti in t]
        ax.plot([L1 * math.cos(theta1) + L2 + L3 * math.cos(theta3) + xi for xi in x],
                [-L1 * math.sin(theta1) + L3 * math.sin(theta3) + yi for yi in y], label="Parabola")
    ax.set_xlabel("Horizontal distance (m)")
    ax.set_ylabel("High Point (m)")
    ax.legend()
    ax.grid()
    st.pyplot(fig)
