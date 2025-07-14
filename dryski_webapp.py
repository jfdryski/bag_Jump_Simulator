
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🚩 通用中文无衬线字体设置（跨平台）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

import zipfile

#字库
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    page_title="JFdryski 滑道滑行模拟器",
    page_icon="🎿",
    layout="centered"
)

# ✅ LOGO & 标题
st.image("JFdryski_logo.png", width=200)
st.title("🎿 JFdryski 气垫跳台滑道滑行模拟器")

st.markdown("""
输入您的参数，点击【开始计算】，并自动生成离线可分享报告！
---
""")

# ✅ 参数输入（可根据您的需求扩展）
摩擦系数 = st.slider("摩擦系数 (0~0.5)", 0.0, 0.5, 0.18, step=0.01)
风阻值 = st.slider("风阻 Cd (0.1~0.9)", 0.1, 0.9, 0.9, step=0.01)
inrun_angle = st.slider("第一段下滑坡角度 (°)", 10, 60, 40)
inrun_length = st.number_input("第一段下滑坡长 (m)", value=43)
transition_length = st.number_input("第二段过渡区长度 (m)", value=10)
kicker_angle = st.slider("第三段上坡角度 (°)", 0, 60, 30)
kicker_length = st.number_input("第三段上坡长 (m)", value=11)

# ✅ 模拟一组计算输出（您可以替换成真实公式）
if st.button("🚀 开始计算"):
    # 👉 假设的计算结果
    result = {
        "第一段结束时速度 (km/h)": [74.3],
        "第二段结束时速度 (km/h)": [56.8],
        "抛物线水平距离 (m)": [21.99],
        "抛物线最大高度 (m)": [3.17],
        "空中飞行时间 (s)": [1.61],
        "全程滑行时间 (s)": [8.18],
        "前台距 Knuckle (m)": [14.29],
    }
    df = pd.DataFrame(result)
    st.success("✅ 计算完成！")
    st.dataframe(df)

    # ✅ 绘制示意图
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot([0, 20, 40, 60], [0, -10, -20, -10], label="下滑段")
    ax.plot([60, 70], [-10, 0], label="抛物线")
    ax.set_title("滑道轨迹示意图")
    ax.set_xlabel("水平距离 (m)")
    ax.set_ylabel("高度 (m)")
    ax.legend()
    st.pyplot(fig)

    # ✅ 保存 PNG
    fig.savefig("dryski_trajectory.png")
    st.success("✅ 已保存轨迹图 dryski_trajectory.png")

    # ✅ 导出参数表 HTML
    df.to_html("dryski_result.html")
    st.success("✅ 已生成参数表 dryski_result.html")

    # ✅ 打包成 ZIP
    with zipfile.ZipFile("dryski_report.zip", "w") as zipf:
        zipf.write("dryski_trajectory.png")
        zipf.write("dryski_result.html")

    with open("dryski_report.zip", "rb") as file:
        st.download_button(
            label="📥 下载完整离线报告 (ZIP)",
            data=file,
            file_name="dryski_report.zip",
            mime="application/zip"
        )

    st.info("离线报告包含：PNG 轨迹图 + HTML 参数表，可直接邮件或微信分享！")


