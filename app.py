import streamlit as st

st.title("Component Procurement System")

component = st.text_input("Component")
model = st.text_input("Model")
spec = st.text_input("Specification")
qty = st.number_input("Quantity", min_value=1)

if st.button("Add Component"):
    st.success("Component Added")