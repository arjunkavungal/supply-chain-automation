import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from io import StringIO
import pandas as pd
from sklearn.linear_model import LinearRegression
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 * 1024 * 1024
@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_a_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      #df = pd.read_csv(StringIO(f))
      df = pd.read_csv(f.filename)
      df['Date'] = pd.to_datetime(df['Date'])
      df['Day'] = df.Date.dt.day
      s = ""
      for i in df['Product'].unique():
        tire = df[df['Product'] == i]
        gb = tire.groupby('Month').count()
        x = [[12],[1],[11],[10],[9]]
        y = gb['Product']
        model = LinearRegression().fit(x, y)
        s += i + str(model.predict([[13]])[0]) # predict for january
      return s
   return s

app.run(host='0.0.0.0',port=81)
