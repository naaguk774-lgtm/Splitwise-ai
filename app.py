import streamlit as st
from PIL import Image
import pandas as pd
import qrcode
import io

st.set_page_config(page_title="SplitWise AI", page_icon="💸")
st.title("💸 SplitWise AI")
st.subheader("Smart Roommates Bill Splitter")

st.write("---")
st.write("📸 **Upload Bill Photo (Optional)**")
uploaded_file = st.file_uploader("Upload your bill image", type=['jpg','png','jpeg'])

if uploaded_file:
    st.image(uploaded_file, width=350, caption="Uploaded Bill")

st.divider()
st.subheader("💰 Split Calculation")

bill_total = st.number_input("Enter Total Amount (in ₹)", value=0.0, min_value=0.0)
num_friends = st.number_input("How Many People?", min_value=1, value=3, step=1)
friends_names = st.text_input("Enter Names (comma separated):", value="You, Ganesh, Ravi")

if st.button("✨ Split Now & Generate QR"):
    if bill_total > 0:
        names = [n.strip() for n in friends_names.split(',') if n.strip()]
        if len(names) < num_friends:
            names = names + [f"Person {i+1}" for i in range(len(names), int(num_friends))]

        per_person = bill_total / len(names)

        st.balloons()
        st.success(f"Each Person Should Pay: ₹{per_person:.2f}")

        df = pd.DataFrame({
            "Name": names,
            "Amount to Pay": [f"₹{per_person:.2f}"]*len(names),
        })
        st.table(df)

        # UPI QR Code
        upi_string = f"upi://pay?pa=yourupi@okaxis&am={per_person:.2f}&cu=INR&tn=SplitWise AI Bill Split"
        qr = qrcode.make(upi_string)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption=f"Scan to Pay ₹{per_person:.2f}", width=250)
        st.caption(f"UPI Link: {upi_string}")

        csv = df.to_csv(index=False)
        st.download_button("📥 Download Split Report (CSV)", csv, "split_report.csv", "text/csv")
    else:
        st.error("Please enter a valid total amount!")

st.caption("Built with AI | Final Year Project Ready")