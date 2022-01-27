from flask import Flask , render_template ,request
import pandas as pd
import numpy as np
app=Flask(__name__)
df=pd.read_csv('car data.csv')
import pickle
model=pickle.load(open("model.pkl","rb"))
@app.route('/')
def home():
    year=sorted(df['Year'].unique())
    fuel_type=df['Fuel_Type'].unique()
    seller_type=df['Seller_Type'].unique()
    transmission=df['Transmission'].unique()
    owner_type=df['Owner'].unique()
    return render_template("index.html",year=year,fuel_type=fuel_type,seller_type=seller_type,transmission=transmission,owner_type=owner_type)
@app.route('/predict',methods=['POST'])
def predict():
    year=int(request.form.get('year'))
    pre_price=float(request.form.get('pre_price'))
    km_driven=float(request.form.get('km_driven'))
    fuel_type=request.form.get('fuel_type')
    if fuel_type=='Petrol':
        fuel=1
    elif fuel_type=='Diesel':
        fuel=0
    else :
        fuel=2
    seller_type=request.form.get('seller_type')
    if seller_type=='Dealer':
        seller=1
    elif seller_type=='Individual':
        seller=0
    transmission=request.form.get('transmission')
    if transmission=='Manual':
        trans=0
    elif transmission=='Automatic':
        trans=1
    owner_type=int(request.form.get('owner_type'))
    final=np.array([year,pre_price,km_driven,fuel,seller,trans,owner_type])
    prediction=model.predict(final.reshape(1,-1))
    output=round(prediction[0],2)
    return render_template('index.html',prediction_text=f'Price would be around rs. {output}Lacs')
if __name__=="__main__":
    app.run(debug=True) 