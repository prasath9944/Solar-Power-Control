import sys,os
from flask import Flask, redirect, request, render_template
import pickle
import serial
import numpy as np
import pandas as pd
from solar_power.predictor import ModelResolver
from solar_power.utils import convert_boolean_toNumerical
from solar_power.logger import logging
from solar_power.exception import SolarException
from solar_power.pipeline.training_pipeline import start_training_pipeline
resolver=ModelResolver()

app=Flask(__name__)



value=[]  
def serialget():
    ser = serial.Serial()
    ser.port = 'COM5'
    ser.baudrate = 9600
    ser.bytesize = 8
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.open()
    v=b'A'
    ser.write(v)
    while True:
        for line in ser.read():
            if chr(line) != '$':
                value.append(chr(line))
            else:
                print("end")
                ser.close()
                return value
def serialset(v):
    ser = serial.Serial()
    ser.port = 'COM5'
    ser.baudrate = 9600
    ser.bytesize = 8
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.open()
    ser.write(v)
    
@app.route('/trainingpipeline')
def training_pipeline():
    if start_training_pipeline()==True:
            return redirect('/')
    else:
        raise ("Production Model is better than Current trained model")
    
                                         
@app.route('/',methods=["GET","POST"])
def home():
    return render_template('index.html')


@app.route('/request1')
def request1():
    str1=''
    print('smb')
    val=[]
    va=serialget()
    print (va)
    for v in va:
        if(v=='*'):
            continue
        else:  
            if(v!='#'): 
                str1+=v
            else:
                print(str1)
                val.append(float(str1))
                str1=""   
    ldr=val[2]
    if(ldr==0):
        ldr=1
    elif(ldr==1):
        ldr=0
    return render_template('templates\index.html',val1=val[0],val2=val[1],val3=ldr)   
    
    
@app.route('/predict',methods=['POST'])

def predict():
    '''
    For rendering results on HTML GUI
    '''
    transformer_file_path=resolver.get_latest_transformer_path()
    model_file_path=resolver.get_latest_model_path()
    transformed=pickle.load(open(transformer_file_path,'rb'))
    model=pickle.load(open(model_file_path,'rb'))

    cat=[]
    col=[]
    
    # int_features = [(x) for x in request.form.values()]
    for x in request.form.items():
            col.append(x[0])
            if x[1].isdigit()!=True:
                cat.append(x[0])
    data=[]
    for x in request.form.values():
        if x.isdigit():
            data.append(float(x))
        else:
            data.append(x)
            
    df=pd.DataFrame(data)
    df=df.transpose()
    df.columns=col
    logging.info(f"The Form has the Details {df}")
    
    logging.info(f"Converting the Categorical feature to Numerical feature using label encoding")
    df=convert_boolean_toNumerical(df,cat)
    
    logging.info(f"Transforming the numpy array and scaling the array")
    transformed_ls=transformed.transform(df.to_numpy())
    
    predicted_value=model.predict(transformed_ls)
    

    output = predicted_value[0]
    logging.info(f"The Predicted output of the solar power is {output}")
    print(output)
    if(output>6982):
        # v=b'B'
        # serialset(v)
        view="Power High"
    elif(output<6982):
        # v=b'C'
        # serialset(v)
        view="Power Low"
    return render_template('index.html', prediction_text='SOLAR POWER IS {}'.format(output),value=view)

if __name__=="__main__":  
    app.run(port=8080,debug=True,host='0.0.0.0')
