import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, send_from_directory, render_template, request
import pandas as pd
import os
import time

app = Flask(__name__, template_folder='.')

# Function to calculate carbon footprint
def calculate_footprint(electricity, transport, waste):
    carbon_footprint = (electricity * 0.5) + (transport * 0.2) + (waste * 0.1)
    suggestions = []
    if electricity > 100:
        suggestions.append("Reduce electricity usage.")
    if transport > 50:
        suggestions.append("Use public transport more often.")
    if waste > 10:
        suggestions.append("Recycle more waste.")
    return carbon_footprint, suggestions

# Function to generate report and chart
def generate_report(electricity, transport, waste):
    data = {
        "Electricity (kWh)": [electricity],
        "Transport (km)": [transport],
        "Waste (kg)": [waste]
    }
    df = pd.DataFrame(data)
    os.makedirs("reports/generated_reports", exist_ok=True)
    df.to_csv("reports/generated_reports/user_report.csv", index=False)
    
    categories = list(data.keys())
    values = [v[0] for v in data.values()]
    
    plt.figure(figsize=(8, 5))
    plt.bar(categories, values)
    plt.title("Carbon Footprint Breakdown")
    plt.ylabel("kg CO2")
    os.makedirs("static/images/charts", exist_ok=True)
    plt.savefig("static/images/charts/carbon_footprint_chart.png")
    plt.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    electricity = float(request.form["electricity"])
    transport = float(request.form["transport"])
    waste = float(request.form["waste"])
    
    carbon_footprint, suggestions = calculate_footprint(electricity, transport, waste)
    generate_report(electricity, transport, waste)
    
    return render_template(
        "index.html",
        carbon_footprint=carbon_footprint,
        suggestions=suggestions,
        timestamp=int(time.time())
    )

if __name__ == "__main__":
    app.run(debug=True)