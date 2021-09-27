import requests
import math
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np
import pickle
import matplotlib.pyplot as plt

from flask import Flask, render_template, g, jsonify, request ,abort
import pandas as pd

app = Flask(__name__)

# Load the model
filename = 'C:/Users/sohai/Desktop/T5 Bootcamp/Linear-Regression-project/website/final_ Aqar_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
districts = ["DISTRICT_أحد","DISTRICT_اخرى","DISTRICT_الاندلس","DISTRICT_البديعة","DISTRICT_الجرادية","DISTRICT_الخالدية","DISTRICT_الخليج","DISTRICT_الدار","DISTRICT_الديرة","DISTRICT_الرمال","DISTRICT_السعادة","DISTRICT_السويدي","DISTRICT_الشرق","DISTRICT_الشميسي","DISTRICT_الصالحية","DISTRICT_العريجاء","DISTRICT_العزيزية","DISTRICT_العيينة","DISTRICT_الفوطة","DISTRICT_الفيحاء","DISTRICT_المرقب","DISTRICT_المروة","DISTRICT_الملز","DISTRICT_الندوة","DISTRICT_النسيم","DISTRICT_النظيم","DISTRICT_اليمامة","DISTRICT_ام","DISTRICT_بدر","DISTRICT_ديراب","DISTRICT_طويق","DISTRICT_ظهرة","DISTRICT_عتيقة","DISTRICT_غبيرة","DISTRICT_منفوحة",]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    district = request.form["district"]
    obj = {
        "BED":request.form["rooms"],
        "BATH": request.form["baths"], 
        "SIZE": request.form["size"]
    }

    for d in districts:
        obj[d] = "1" if district == d else "0"


    obj["BED2"] = int(request.form["rooms"]) ** 2
    obj["BATH2"] =  int(request.form["baths"]) ** 2
    obj["SIZE2"] = int(request.form["size"]) ** 2
    
    x_df = pd.DataFrame([obj])

    result = loaded_model.predict(x_df)
    data = {"result": int(result[0])}

    return data

"""
Error handlers
"""
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "We couldn't find what you are looking for!"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Your request is not well formated!"
    }), 400


@app.errorhandler(500)
def unprocessable_entity(error):
    return jsonify({
        "success": False,
        "message": "Sorry, we coludn't proccess your request. ERROR during prediction"
    }), 500

if __name__ == "__main__":
    app.run(debug=True)

