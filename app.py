from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load your CSV file
CSV_FILE = "OCD_Patient.csv"
df = pd.read_csv(CSV_FILE)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    patient_id = request.form.get("patient_id")
    age = request.form.get("age")
    gender = request.form.get("gender")

    filtered = df.copy()

    # If PatientID provided → only one patient
    if patient_id:
        filtered = filtered[filtered['PatientID'].astype(str) == patient_id]
    else:
        if age:
            filtered = filtered[filtered['Age'] == int(age)]
        if gender:
            filtered = filtered[filtered['Gender'].str.lower() == gender.lower()]

    patients = filtered.to_dict(orient="records")
    return render_template('result.html', patients=patients)

@app.route('/patient/<patient_id>')
def patient_detail(patient_id):
    patient = df[df['PatientID'].astype(str) == str(patient_id)]
    if patient.empty:
        return "Patient not found", 404
    patient = patient.iloc[0].to_dict()
    return render_template('patient_detail.html', patient=patient)

if __name__ == "__main__":
    app.run(debug=True)
