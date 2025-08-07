import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
from datetime import datetime

st.set_page_config(page_title="Lab & Notes Viewer", layout="wide")
st.title("🩺 Lab & Notes Viewer")

# === Upload Section ===
st.sidebar.header("📁 Upload Lab CSV")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])
    st.success("✅ CSV uploaded successfully.")
    st.info("⬅️ Use the sidebar to filter by patient and date")

    # === Tabs Layout ===
    tab1, tab2 = st.tabs(["🧪 Lab Viewer", "📝 Notes"])

    # === TAB 1: LAB VIEWER ===
    with tab1:
        st.sidebar.markdown("---")
        st.sidebar.header("🔍 Filter Options")
        patient_list = df["Patient"].unique()
        selected_patient = st.sidebar.selectbox("Select Patient", patient_list)

        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=[df["Date"].min(), df["Date"].max()]
        )

        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        df = df[(df["Patient"] == selected_patient) & (df["Date"].between(start, end))]

        st.markdown("---")
        st.subheader("🧾 Filtered Lab Results")
        st.dataframe(df)

        chart_type = st.radio("📊 Select Chart Type:", ["Line", "Bar"], horizontal=True)

        # Alerts
        low_hb = df[df["Hb"] < 10] if "Hb" in df.columns else pd.DataFrame()
        low_plt = df[df["PLT"] < 150] if "PLT" in df.columns else pd.DataFrame()

        if not low_hb.empty or not low_plt.empty:
            st.subheader("⚠️ Alerts")
            for _, row in low_hb.iterrows():
                st.warning(f"Hb {row['Hb']} on {row['Date'].date()} is low.")
            for _, row in low_plt.iterrows():
                st.warning(f"PLT {row['PLT']} on {row['Date'].date()} is low.")
        else:
            st.success("✅ No critical lab alerts")

        # Plot Trends
        for lab in ["Hb", "PLT", "WBC"]:
            if lab in df.columns:
                st.subheader(f"{lab} Trend")
                fig, ax = plt.subplots()

                if chart_type == "Line":
                    ax.plot(df["Date"], df[lab], marker="o")
                else:
                    ax.bar(df["Date"].dt.strftime("%Y-%m-%d"), df[lab])

                if lab == "Hb":
                    ax.axhline(10, color="red", linestyle="--", label="Hb < 10")
                elif lab == "PLT":
                    ax.axhline(150, color="orange", linestyle="--", label="PLT < 150")

                ax.set_xlabel("Date")
                ax.set_ylabel(lab)
                ax.legend()
                ax.grid(True)
                st.pyplot(fig)

        # Export
        st.download_button(
            label="📥 Download Filtered Table as CSV",
            data=df.to_csv(index=False),
            file_name=f"{selected_patient}_labs.csv",
            mime="text/csv"
        )

    # === TAB 2: NOTES ===
    with tab2:
        st.markdown("---")
        st.subheader("📝 Add a Clinical Note")

        note_patient = selected_patient
        note_date = st.date_input("Note Date", value=df["Date"].max())
        note_text = st.text_area("Enter Note", height=150)

        if st.button("💾 Save Note"):
            os.makedirs("patient_notes", exist_ok=True)
            safe_name = note_patient.lower().replace(" ", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"note_{safe_name}_{timestamp}.txt"
            filepath = os.path.join("patient_notes", filename)

            with open(filepath, "w") as f:
                f.write(f"Patient: {note_patient}\n")
                f.write(f"Date: {note_date}\n\n")
                f.write(note_text)

            st.success(f"📝 Note saved for {note_patient} on {note_date}")

        st.markdown("---")
        st.subheader("📂 View Saved Notes")

        safe_name = selected_patient.lower().replace(" ", "_")
        note_files = glob.glob(f"patient_notes/note_{safe_name}_*.txt")

        if not note_files:
            st.info("No saved notes found for this patient.")
        else:
            for file_path in sorted(note_files, reverse=True):
                with open(file_path, "r") as f:
                    content = f.read()
                filename = os.path.basename(file_path)
                st.expander(f"🗂 {filename}").write(content)

else:
    st.info("⬅️ Please upload a lab CSV to begin.")
