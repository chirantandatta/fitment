import os
import warnings
from flask import Flask, render_template, url_for, request, redirect,session
import pandas as pd
import nltk
nltk.download("all")
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from gtts import gTTS
import wikipedia
import joblib
import re
import playsound
g=joblib.load('models/prediction.pkl')
t=joblib.load('models/transform.pkl')
def clean(x):
  
    x = re.sub("\'", "", x) 
    
    x = re.sub("[^a-zA-Z]"," ",x) 

    x= ' '.join(x.split()) 
    
    x = x.lower() 
    
    return x
stop_words = set(stopwords.words('english'))
def removestopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)
l=WordNetLemmatizer()
def lemmatizes(text):
  lem=[l.lemmatize(w) for w in text.split()]
  return ' '.join(lem)


warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
p=''
# secret key is needed for session
@app.route('/',  methods=['GET', 'POST'])
def home():
    return render_template('index.html',genre=p)
@app.route('/prediction')
def prediction():
 try:
    bookname = session['bookname']
    r=wikipedia.page(bookname).content
    p=[]
    q=[]
    p.append(bookname)
    q.append(r)
    df3=pd.DataFrame({'title':p,'summary':q})
    df3.loc[:,'summary']=df3.loc[:,'summary'].apply(lambda x: clean(x))
    df3['summary'] = df3['summary'].apply(lambda x: removestopwords(x))
    df3['summary'] = df3['summary'].apply(lambda x: lemmatizes(x))
    x8=df3['summary']
    x8=t.transform(x8)
    y8=g.predict(x8)
    k=y8[0]
    m=k
    f="The category of book is "+m
    n="The name of book  is "+"'"+bookname+"'"
    display="Thank You.Here is the information provided"
    tts=gTTS(f,lang='en')
    files="summarys.mp3"
    tts.save(files)
    os.remove(files)
    return render_template('predict.html',display=display,book=n,category=f)
 except:
    display="Either invalid data or could not get the required information"
    n=""
    f=""
    return render_template('predict.html',display=display,book=n,category=f)
    

@app.post('/book')
def bookgenre():
    session['bookname']=request.form.get('book')
    return redirect(url_for("prediction"))
port=int(os.environ.get("PORT",2000))
app.run(host='0.0.0.0',port=port)