from copyreg import pickle
from flask import Flask,render_template, request, redirect
import os,pickle
from PIL import Image
import numpy as np


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('method.html')

@app.route('/user/<username>')
def show_user(username):
    return username + '!!!'

@app.route('/user/<username>/<int:age>')
def show_user_age(username,age):
    return username + ':'+ str(age)

# request object
# Form(post,딕셔너리),args(get,?뒤에 있는 값 파싱),files,method(post,get,...)

@app.route('/method',methods=['GET','POST'])
def method_test():
    if request.method == 'POST':
        return render_template('show_result.html',data=request.form)
    else:
        return render_template('show_result.html',data=request.args)

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=='GET':
        return render_template('fileup.html')
    else:
        f = request.files['file']
        path = os.path.dirname(__file__)+'/upload/'+f.filename
        print(path)
        f.save(path)
        return redirect('/')

@app.route('/mnist',methods=['GET','POST'])
def mnist():
    if request.method =='GET':
        return render_template('mnistform.html')
    else:
        f= request.files['filename']
        path = os.path.dirname(__file__)+'/static/upload/'+ f.filename
        print(path)
        f.save(path)
        img = Image.open(path).convert('L')
        img = np.resize(img,(1,784))
        img = 255-(img)
        path = 'static/upload/'+ f.filename
        modelpath = 'model.data'
        f = open(modelpath,'rb') 
        model = pickle.load(f)
        pred = model.predict(img)
        print(pred)
        return render_template('mnistresult.html',data=[pred[0],path])



if __name__ == '__main__':
    app.run(debug=True,port=80)