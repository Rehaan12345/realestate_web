from flask import Blueprint, render_template, redirect, request, flash, url_for, send_file
from .scraper2 import run
import pandas as pd
from io import BytesIO

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form.get("category") and request.form.get("location") and request.form.get("searchamount"):
            category = request.form.get("category")
            location = request.form.get("location")
            search_amount = request.form.get("searchamount")

            run(category=category, location=location, search_amount=int(search_amount)) # Source: https://www.youtube.com/watch?v=5vmV5Jc9nI0&list=TLPQMDEwMTIwMjSg9kSWpGkwdA&index=1

            data  = pd.read_csv("google_maps_data.csv")

            return render_template("layout.html", tables=[data.to_html()], titles=[""], category=category, location=location)
        if request.form.get("downloadcsv"): 
            return send_file("../google_maps_data.csv", download_name="data.csv", as_attachment=True)
        if request.form.get("downloadexcel"): 
            return send_file("../google_maps_data.xlsx", download_name="data.xlsx", as_attachment=True)

    data  = pd.read_csv("google_maps_data.csv")
    category = "Category"
    location = "Location"
    return render_template("layout.html", tables=[data.to_html()], titles=[""], category=category, location=location)