from flask import Flask, render_template, request
import math
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
            weight = float(weight)
            cbodyfat = float(cbodyfat)
            gbodyfat = float(gbodyfat)
            rate = float(rate)
            clean_mass = weight*(100-cbodyfat)/100
            glean_mass = clean_mass*.97
            goal_weight = glean_mass/((100-gbodyfat)/100)
            tt6 = math.ceil((weight-goal_weight)/rate)
            clean_mass = round(clean_mass, 2)
            glean_mass = round(glean_mass, 2)
            goal_weight = round(goal_weight, 2)
            return render_template('index.html', clean_mass = clean_mass, glean_mass = glean_mass, goal_weight = goal_weight, tt6 = tt6)
        else:
            return 'Error: one or more inputs was not a number'

if __name__ == "__main__":
    app.run(debug=True)
