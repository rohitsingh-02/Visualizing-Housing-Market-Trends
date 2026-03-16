from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# -----------------------------
# Load Dataset
# -----------------------------

data = pd.read_csv("Transformed_Housing_Data2.csv")

# Clean column names
data.columns = (
    data.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
)

print("Columns:", data.columns)

# -----------------------------
# Calculated Fields
# -----------------------------

if "Sale_Price" in data.columns and "Flat_Area_in_Sqft" in data.columns:
    data["Price_per_sqft"] = data["Sale_Price"] / data["Flat_Area_in_Sqft"]

if "No_of_Bedrooms" in data.columns:
    data["Price_per_Bedroom"] = data["Sale_Price"] / data["No_of_Bedrooms"]

if "No_of_Bathrooms" in data.columns:
    data["Price_per_Bathroom"] = data["Sale_Price"] / data["No_of_Bathrooms"]

if "Flat_Area_in_Sqft" in data.columns and "Lot_Area_in_Sqft" in data.columns:
    data["Total_Area"] = data["Flat_Area_in_Sqft"] + data["Lot_Area_in_Sqft"]

# Price category
def price_category(price):
    if price < 200000:
        return "Low"
    elif price < 500000:
        return "Medium"
    else:
        return "High"

if "Sale_Price" in data.columns:
    data["Price_Category"] = data["Sale_Price"].apply(price_category)

# -----------------------------
# KPI Metrics
# -----------------------------

total_houses = len(data)

avg_price = round(data["Sale_Price"].mean(),2) if "Sale_Price" in data.columns else 0

avg_area = round(data["Flat_Area_in_Sqft"].mean(),2) if "Flat_Area_in_Sqft" in data.columns else 0

avg_bedrooms = round(data["No_of_Bedrooms"].mean(),2) if "No_of_Bedrooms" in data.columns else 0

# -----------------------------
# Create chart folder
# -----------------------------

os.makedirs("static/charts", exist_ok=True)

# -----------------------------
# Visualization 1
# Price Distribution
# -----------------------------

if "Sale_Price" in data.columns:
    plt.figure(figsize=(6,4))
    sns.histplot(data["Sale_Price"], bins=30)
    plt.title("Sale Price Distribution")
    plt.savefig("static/charts/price_distribution.png")
    plt.close()

# -----------------------------
# Visualization 2
# Bedrooms vs Price
# -----------------------------

if "No_of_Bedrooms" in data.columns:
    plt.figure(figsize=(6,4))
    sns.barplot(x="No_of_Bedrooms", y="Sale_Price", data=data)
    plt.title("Bedrooms vs Price")
    plt.savefig("static/charts/bedroom_price.png")
    plt.close()

# -----------------------------
# Visualization 3
# Area vs Price
# -----------------------------

if "Flat_Area_in_Sqft" in data.columns:
    plt.figure(figsize=(6,4))
    sns.scatterplot(x="Flat_Area_in_Sqft", y="Sale_Price", data=data)
    plt.title("Area vs Price")
    plt.savefig("static/charts/area_price.png")
    plt.close()

# -----------------------------
# Visualization 4
# Floors vs Price
# -----------------------------

if "No_of_Floors" in data.columns:
    plt.figure(figsize=(6,4))
    sns.barplot(x="No_of_Floors", y="Sale_Price", data=data)
    plt.title("Floors vs Price")
    plt.savefig("static/charts/floors_price.png")
    plt.close()

# -----------------------------
# Visualization 5
# Renovation Impact
# -----------------------------

if "Ever_Renovated" in data.columns:
    plt.figure(figsize=(6,4))
    sns.barplot(x="Ever_Renovated", y="Sale_Price", data=data)
    plt.title("Renovation Impact")
    plt.savefig("static/charts/renovation_price.png")
    plt.close()

# -----------------------------
# Visualization 6
# Condition vs Price
# -----------------------------

if "Overall_Condition" in data.columns:
    plt.figure(figsize=(6,4))
    sns.barplot(x="Overall_Condition", y="Sale_Price", data=data)
    plt.title("Condition vs Price")
    plt.savefig("static/charts/condition_price.png")
    plt.close()

# -----------------------------
# Visualization 7
# Grade vs Price
# -----------------------------

if "Overall_Grade" in data.columns:
    plt.figure(figsize=(6,4))
    sns.barplot(x="Overall_Grade", y="Sale_Price", data=data)
    plt.title("Grade vs Price")
    plt.savefig("static/charts/grade_price.png")
    plt.close()

# -----------------------------
# Visualization 8
# House Age vs Price
# -----------------------------

if "Age_of_House_in_Years" in data.columns:
    plt.figure(figsize=(6,4))
    sns.scatterplot(x="Age_of_House_in_Years", y="Sale_Price", data=data)
    plt.title("Age vs Price")
    plt.savefig("static/charts/age_price.png")
    plt.close()

# -----------------------------
# Tableau Dashboard
# -----------------------------

TABLEAU_URL = "https://public.tableau.com/views/HousingDashboard/Dashboard1"

# -----------------------------
# Flask Route
# -----------------------------

@app.route("/")
def home():

    table_data = data.head(20).to_dict(orient="records")

    return render_template(
        "index.html",
        total_houses=total_houses,
        avg_price=avg_price,
        avg_area=avg_area,
        avg_bedrooms=avg_bedrooms,
        table_data=table_data,
        tableau_url=TABLEAU_URL
    )

# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)