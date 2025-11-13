import streamlit as st

st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

st.title("Calculator")

# Input fields
num1 = st.number_input("Enter first number:", value=0.0, step=1.0)
num2 = st.number_input("Enter second number:", value=0.0, step=1.0)

# Operation selection
operation = st.selectbox("Select operation:", ["+", "-", "*", "/"])

# Perform calculation instantly
if operation == "+":
    result = num1 + num2
elif operation == "-":
    result = num1 - num2
elif operation == "*":
    result = num1 * num2
elif operation == "/":
    result = "Cannot divide by zero" if num2 == 0 else num1 / num2
else:
    result = "Invalid operation"

# Display result
st.markdown("### ✅ Result:")
st.success(result)
