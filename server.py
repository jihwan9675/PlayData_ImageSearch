"""
마지막 수정 : 12.11.13
작성자 : 신지환
내용 : 플레이데이터 미니프로젝트(이미지로 해당 장소 정보 얻기)
이 코드는 3개의 파트가 있다.
1. 웹서버 열기
2. 예측
3. 출력 (load result.html)
그리고 3개의 자체 모듈이 있다.
modules. load_name, preproceess, build_model
"""

from flask import Flask,Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
import os,csv,cv2, sys, numpy,h5py, time
from modules.load_name import load_name
from modules.preprocess import preprocess
from modules.build_model import build_model

Place_Name = dict() # 랜드마크 이름
model=0 # 예측 모델
app = Flask(__name__)

@app.route('/')
def uploadHTML():
    return redirect(url_for('static', filename='upload.html'))
    
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 이미지를 현재 시간을 이름으로 저장
        now = time.localtime()
        imageName=str(now.tm_hour)+str(now.tm_min)+str(now.tm_sec)+str(".jpg") 
        f = request.files['file']
        f.save("./static/uploader/"+imageName)
        print("Saved File : "+"./static/uploader/"+imageName)

        # 예측
        img=preprocess("./static/uploader/"+imageName) #전처리
        prediction = model.predict(img, verbose=1)
        max_value=max(prediction[0])
        print(max_value)

        if max_value<0.6:
            return render_template('cannot_find.html', name="./uploader/"+imageName)
        ###
        ### 여기에 모델이 아직 학습이 안된 경우 제외하는 코드 추가할 예정 ... 20.11.13(신지환)
        ###
        idx = numpy.where(prediction[0]==max_value)[0][0]
        s = Place_Name[str(idx)]
        print(s) # 결과

        return render_template('search_place.html', name="./uploader/"+imageName, diease=s)
        
    
if __name__=='__main__':
    Place_Name = load_name("category.csv") # 랜드마크 Dictionary 생성 --> (idx, Name)
    model = build_model(1049)
    app.run(host="0.0.0.0", port="80", debug=True)