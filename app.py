from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

data = pd.read_csv("Transformed_Housing_Data2.csv")

data.columns = (
    data.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
)

if "Sale_Price" in data.columns and "Flat_Area_in_Sqft" in data.columns:
    data["Price_per_sqft"] = data["Sale_Price"] / data["Flat_Area_in_Sqft"]

if "No_of_Bedrooms" in data.columns:
    data["Price_per_Bedroom"] = data["Sale_Price"] / data["No_of_Bedrooms"]

if "No_of_Bathrooms" in data.columns:
    data["Price_per_Bathroom"] = data["Sale_Price"] / data["No_of_Bathrooms"]

if "Flat_Area_in_Sqft" in data.columns and "Lot_Area_in_Sqft" in data.columns:
    data["Total_Area"] = data["Flat_Area_in_Sqft"] + data["Lot_Area_in_Sqft"]

def price_category(price):
    if price < 200000:
        return "Low"
    elif price < 500000:
        return "Medium"
    else:
        return "High"

if "Sale_Price" in data.columns:
    data["Price_Category"] = data["Sale_Price"].apply(price_category)

os.makedirs("static/charts", exist_ok=True)

TABLEAU_URL = "https://public.tableau.com/views/HousingDashboard/Dashboard1"

@app.route("/", methods=["GET"])
def home():

    filtered_data = data.copy()

    bedrooms = request.args.get("bedrooms")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    if bedrooms:
        filtered_data = filtered_data[filtered_data["No_of_Bedrooms"] == int(bedrooms)]

    if min_price:
        filtered_data = filtered_data[filtered_data["Sale_Price"] >= int(min_price)]

    if max_price:
        filtered_data = filtered_data[filtered_data["Sale_Price"] <= int(max_price)]

    total_houses = len(filtered_data)
    avg_price = round(filtered_data["Sale_Price"].mean(),2) if len(filtered_data)>0 else 0
    avg_area = round(filtered_data["Flat_Area_in_Sqft"].mean(),2) if len(filtered_data)>0 else 0
    avg_bedrooms = round(filtered_data["No_of_Bedrooms"].mean(),2) if len(filtered_data)>0 else 0

    plt.figure(figsize=(6,4))
    sns.histplot(filtered_data["Sale_Price"], bins=30)
    plt.title("Price Distribution")
    plt.savefig("static/charts/price_distribution.png")
    plt.close()

    plt.figure(figsize=(6,4))
    sns.barplot(x="No_of_Bedrooms", y="Sale_Price", data=filtered_data)
    plt.title("Bedrooms vs Price")
    plt.savefig("static/charts/bedroom_price.png")
    plt.close()

    plt.figure(figsize=(6,4))
    sns.scatterplot(x="Flat_Area_in_Sqft", y="Sale_Price", data=filtered_data)
    plt.title("Area vs Price")
    plt.savefig("static/charts/area_price.png")
    plt.close()

    plt.figure(figsize=(6,4))
    sns.barplot(x="No_of_Floors", y="Sale_Price", data=filtered_data)
    plt.title("Floors vs Price")
    plt.savefig("static/charts/floors_price.png")
    plt.close()

    if "Ever_Renovated" in filtered_data.columns:
        plt.figure(figsize=(6,4))
        sns.barplot(x="Ever_Renovated", y="Sale_Price", data=filtered_data)
        plt.title("Renovation Impact")
        plt.savefig("static/charts/renovation_price.png")
        plt.close()

    table_data = filtered_data.head(20).to_dict(orient="records")

    # return render_template(
    #     "index.html",
    #     total_houses=total_houses,
    #     avg_price=avg_price,
    #     avg_area=avg_area,
    #     avg_bedrooms=avg_bedrooms,
    #     table_data=table_data,
    #     tableau_url=TABLEAU_URL
    # )

if __name__ == "__main__":
    app.run(debug=True)