from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#form submission
@app.route('/send', methods = ['POST'])
def send():
    if request.method == 'POST':
        weight = request.form['weight']
        cbodyfat = request.form['cbodyfat']
        gbodyfat = request.form['gbodyfat']
        rate = request.form['rate']


        if weight.isdigit() and cbodyfat.isdigit() and gbodyfat.isdigit() and rate.isdigit():
            lean_mass = weight *(100-cbodyfat)
            return render_template('index.html', lean_mass = lean_mass)
        else:
            return 'Error: one or more inputs was not a number'

if __name__ == "__main__":
    app.run(debug=True)
