import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' to avoid Tkinter issues
import matplotlib.pyplot as plt

from flask import Flask, render_template, request
import pandas as pd
import os
import time

app = Flask(__name__)

# Function to calculate carbon footprint
def calculate_footprint(electricity, transport, waste):
    # Simple carbon footprint calculation (example)
    carbon_footprint = (electricity * 0.5) + (transport * 0.2) + (waste * 0.1)
    
    # Suggestions
    suggestions = []
    if electricity > 100:
        suggestions.append("Reduce electricity usage.")
    if transport > 50:
        suggestions.append("Use public transport more often.")
    if waste > 10:
        suggestions.append("Recycle more waste.")
    
    return carbon_footprint, suggestions

# Function to generate a report and chart
def generate_report(electricity, transport, waste):
    # Save data to CSV
    data = {
        "Electricity (kWh)": [electricity],
        "Transport (km)": [transport],
        "Waste (kg)": [waste]
    }
    df = pd.DataFrame(data)
    df.to_csv("reports/generated_reports/user_report.csv", index=False)
    
    # Generate a simple bar chart
    categories = list(data.keys())  # Convert keys to a list
    values = list(data.values())    # Convert values to a list
    
    # Flatten the values list (since each value is a single-element list)
    values = [v[0] for v in values]
    
    plt.bar(categories, values)  # Pass lists to plt.bar()
    plt.title("Carbon Footprint Breakdown")
    plt.ylabel("kg CO2")
    plt.savefig("static/images/charts/carbon_footprint_chart.png")
    plt.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    electricity = float(request.form["electricity"])
    transport = float(request.form["transport"])
    waste = float(request.form["waste"])
    
    carbon_footprint, suggestions = calculate_footprint(electricity, transport, waste)
    generate_report(electricity, transport, waste)
    
    # Generate a timestamp to prevent browser caching
    timestamp = int(time.time())
    
    return render_template("index.html", carbon_footprint=carbon_footprint, suggestions=suggestions, timestamp=timestamp)

if __name__ == "__main__":
    # Create necessary directories if they don't exist
    os.makedirs("reports/generated_reports", exist_ok=True)
    os.makedirs("static/images/charts", exist_ok=True)
    
    app.run(debug=True)