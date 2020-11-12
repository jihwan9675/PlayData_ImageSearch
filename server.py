# from flask import Flask
from flask import Flask,Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
# import tensorflow as tf
import os,csv,cv2, sys, numpy,h5py, time
from modules.load_name import load_name
from modules.preprocess import preprocess
from modules.build_model import build_model

Place_Name = dict() # 랜드마크 이름

app = Flask(__name__)
model=0

state = -1

@app.route('/')
def uploadHTML():
    #return render_template('index.html')
    return redirect(url_for('static', filename='upload.html'))
    
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        now = time.localtime()
        strss=str(now.tm_hour)+str(now.tm_min)+str(now.tm_sec)+str(".jpg")
        f = request.files['file']
        f.save("./static/uploader/"+strss)
        print("Saved File : "+"./static/uploader/"+strss)
        img=preprocess("./static/uploader/"+strss)
        prediction = model.predict(img, verbose=1)
        max_value=max(prediction[0])
        print(max_value)
        idx = numpy.where(prediction[0]==max_value)[0][0]
        s = Place_Name[str(idx)]
        print(s)
        #idx = predict(img)

        return render_template('resulttest.html', name="./uploader/"+strss, diease=s)
        
    
if __name__=='__main__':
    #model = load_weights("./Weight/place_weight.h5")
    Place_Name = load_name("category.csv") # Dictionary 생성
    model = build_model(1049)
    app.run(host="127.0.0.1", port="80", debug=True)