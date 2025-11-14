import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

def add_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
              linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)),
              url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .app-card {{
            max-width: 680px;
            margin: 48px auto;
            padding: 28px 28px 36px;
            background: rgba(255,255,255,0.96);
            color: #111827;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            backdrop-filter: blur(2px);
        }}
        .app-card h1, .app-card h2, .app-card h3 {{ color: #0f172a; }}
        .app-card input {{ background:#fff !important; color:#111827 !important; border:1px solid #e5e7eb !important; border-radius:10px !important; }}
        .app-card label {{ color:#111827 !important; font-weight:600 !important; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use your image file name here
add_bg("bmi_bg.jpg")

def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

st.markdown('<div class="app-card">', unsafe_allow_html=True)

st.title("⚖️ BMI (Body Mass Index) Calculator")
st.subheader("Enter your details")

col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("Weight (kg):", min_value=0.0, step=0.1)
with col2:
    height = st.number_input("Height (cm):", min_value=0.0, step=0.1)

bmi = 0 if height <= 0 else round(weight / ((height / 100) ** 2), 2)

if weight > 0 and height > 0:
    st.subheader("Your BMI Result")
    st.success(f"Your BMI is: **{bmi}**  |  Category: **{bmi_category(bmi)}**")
    cat = bmi_category(bmi)
    if cat == "Underweight":
        st.warning("You are underweight 🟡")
    elif cat == "Normal":
        st.info("You have a normal weight 🟢")
    elif cat == "Overweight":
        st.warning("You are overweight 🟠")
    else:
        st.error("You are obese 🔴")
else:
    st.info("Please enter both weight and height to calculate BMI.")

st.markdown("### 📊 BMI Classification Pie Chart")

# --- Mode switch: single vs multiple people ---
multi = st.checkbox("Track multiple people")

if not multi:
    # Single-user pie: one slice showing the user’s category
    labels = ["Underweight", "Normal", "Overweight", "Obese"]
    sizes = [0, 0, 0, 0]
    if weight > 0 and height > 0:
        idx = labels.index(bmi_category(bmi))
        sizes[idx] = 1
    else:
        # If no input yet, show equal placeholders
        sizes = [1, 1, 1, 1]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct=lambda p: f"{p:.0f}%" if p > 0 else "", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

else:
    st.caption("Enter names with weight (kg) and height (cm). BMI & category are computed automatically.")
    df = st.data_editor(
        pd.DataFrame({"Name": ["Person 1", "Person 2"],
                      "Weight (kg)": [70.0, 85.0],
                      "Height (cm)": [170.0, 175.0]}),
        use_container_width=True,
        num_rows="dynamic"
    )

    if len(df) == 0:
        st.warning("Add at least one person to see the pie chart.")
    else:
        # Compute BMI and category for each row if values are valid
        def compute_row(row):
            try:
                w = float(row["Weight (kg)"])
                h = float(row["Height (cm)"])
                if h <= 0:
                    return pd.Series({"BMI": None, "Category": None})
                b = round(w / ((h/100)**2), 2)
                return pd.Series({"BMI": b, "Category": bmi_category(b)})
            except Exception:
                return pd.Series({"BMI": None, "Category": None})

        out = df.apply(compute_row, axis=1)
        df = pd.concat([df, out], axis=1)
        st.dataframe(df, use_container_width=True)

        counts = df["Category"].value_counts(dropna=True).reindex(["Underweight","Normal","Overweight","Obese"]).fillna(0)
        if counts.sum() == 0:
            st.info("Enter valid weights and heights to compute BMI.")
        else:
            fig, ax = plt.subplots()
            ax.pie(counts.values,
                   labels=counts.index,
                   autopct=lambda p: f"{p:.0f}%" if p > 0 else "",
                   startangle=90)
            ax.axis("equal")
            st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)
