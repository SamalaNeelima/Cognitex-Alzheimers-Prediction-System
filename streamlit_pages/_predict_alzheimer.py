import os
import re
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import io
from fpdf import FPDF
import mysql.connector

# ✅ Connect to MySQL Database
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your MySQL username
        password="root",  # Change to your MySQL password
        database="patient_db"
    )
    print("✅ Database connection successful!")
except mysql.connector.Error as err:
    st.error(f"❌ Error connecting to database: {err}")
    exit(1)

mycursor = mydb.cursor()


# ✅ Load the Model
MODEL_PATH = "model/my_model.h5"
if not os.path.exists(MODEL_PATH):
    st.error("⚠️ Model file not found! Please check the path.")
    st.stop()
model = load_model(MODEL_PATH)

# ✅ Validation Functions
def validate_phone_number(phone_number):
    """Ensures phone number is valid (10-15 digits)."""
    pattern = r'^\+?\d{10,15}$'
    if not re.match(pattern, str(phone_number)):
        st.error("⚠️ Please enter a valid phone number!")
        return False
    return True

def validate_name(name):
    """Checks if name contains only letters and spaces."""
    if not all(char.isalpha() or char.isspace() for char in name):
        st.error("⚠️ Name should not contain numbers or special characters.")
        return False
    return True

def validate_input(name, age, contact, file):
    """Ensures all fields are filled."""
    if not name or not age or not contact or not file:
        st.error("⚠️ All fields are required!")
        return False
    return True

# ✅ Image Processing
def preprocess_image(image):
    """Resizes and normalizes MRI image for model prediction."""
    image = image.convert('RGB').resize((176, 176))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)

# ✅ Model Prediction
def predict_alzheimer(image):
    """Predicts Alzheimer's stage based on the MRI scan."""
    prediction = model.predict(image)
    return np.argmax(prediction, axis=1)[0]



# ✅ Insert Data into MySQL
def insert_data(patient_name, age, gender, mobile_no, prediction, image):
    """Stores patient details and MRI scan in MySQL database."""
    try:
        
        sql = "INSERT INTO predicts (name, age, gender, contact, diagnosis_condition, image) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (patient_name, age, gender, mobile_no, prediction)
        mycursor.execute(sql, val)
        mydb.commit()
        print("✅ Record inserted successfully!")
    except mysql.connector.Error as err:
        print("❌ Error inserting record:", err)

# ✅ Generate PDF Report
def generate_pdf(patient_name, age, gender, mobile_no, condition):
    """Creates a downloadable PDF report for the patient."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Alzheimer's Disease Prediction Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Patient Name: {patient_name}", ln=True)
    pdf.cell(200, 10, f"Age: {age}", ln=True)
    pdf.cell(200, 10, f"Gender: {gender}", ln=True)
    pdf.cell(200, 10, f"Contact: {mobile_no}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Diagnosis:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Predicted Condition: {condition}", ln=True)
    pdf.ln(10)

    if condition != "No Dementia":
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Precautions:", ln=True)
        pdf.set_font("Arial", size=12)
        precautions = [
            "Maintain a daily routine.",
            "Stay physically and mentally active.",
            "Follow a healthy diet.",
            "Engage in social interactions.",
            "Reduce stress and anxiety.",
            "Get enough sleep every night.",
            "Stay hydrated and avoid alcohol.",
            "Take prescribed medications on time."
        ]
        for precaution in precautions:
            pdf.multi_cell(0, 8, f"- {precaution}")
        pdf.ln(10)
    else:
        pdf.cell(200, 10, "🎉 Congratulations! No Dementia Detected.", ln=True)

    temp_img_path = "temp_mri_scan.jpg"
    mri_image.resize((200, 200)).save(temp_img_path)
    pdf.image(temp_img_path, x=30, w=150)

    pdf_file_path = "Alzheimer_Report.pdf"
    pdf.output(pdf_file_path)

    with open(pdf_file_path, "rb") as f:
        return f.read()

# ✅ Streamlit UI
def prediction_page():
    """Main UI for Alzheimer's Prediction System."""
    st.title("🧠 Alzheimer's Prediction System")
    patient_name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=122, step=1, value=65)
    gender = st.selectbox("Gender", ("Male", "Female"))
    mobile_no = st.text_input("Mobile Number")
    mri_scan = st.file_uploader("Upload MRI Scan (JPG/PNG)", type=["jpg", "jpeg", "png"])

    if st.button("Submit & Predict"):
        if validate_name(patient_name) and validate_phone_number(mobile_no) and validate_input(patient_name, age, mobile_no, mri_scan):
            image = Image.open(mri_scan)
            preprocessed_image = preprocess_image(image)
            predicted_condition = predict_alzheimer(preprocessed_image)

            CONDITION_LABELS = {0: "Mild Dementia", 1: "Moderate Dementia", 2: "No Dementia", 3: "Very Mild Dementia"}
            condition = CONDITION_LABELS.get(predicted_condition, "Unknown Condition")

            # ✅ Save Patient Data in Database
            insert_data(patient_name, age, gender, mobile_no, condition)

            # ✅ Show Prediction Result
            st.success(f"✅ Prediction Complete! Patient Condition: **{condition}**")

            # ✅ Generate & Download PDF Report
            pdf_bytes = generate_pdf(patient_name, age, gender, mobile_no, condition, image)
            st.download_button("📄 Download Report", pdf_bytes, "Alzheimer_Report.pdf", "application/pdf")

# ✅ Run Streamlit App
if __name__ == "__main__":
    prediction_page()
