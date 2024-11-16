import pickle
from flask import Flask, render_template, request

#Create an object of the class flask
app = Flask(__name__)
model = pickle.load(open('derma.pkl','rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = model.predict([[request.form.get('user_id')]])
    print(prediction)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
