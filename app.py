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


        if weight.isdigit() and cbodyfat.isdigit() and gbodyfat.isdigit():
            weight = float(weight)
            cbodyfat = float(cbodyfat)
            gbodyfat = float(gbodyfat)
            clean_mass = weight*(100-cbodyfat)/100
            glean_mass = clean_mass*.97
            goal_weight = glean_mass/((100-gbodyfat)/100)
            slow_rate = weight*.0075
            fast_rate = weight*.01
            slow_tt6 = math.ceil((weight-goal_weight)/slow_rate)
            fast_tt6 = math.ceil((weight-goal_weight)/fast_rate)
            calories = int(weight*12)
            clean_mass = round(clean_mass, 2)
            glean_mass = round(glean_mass, 2)
            goal_weight = round(goal_weight, 2)
            return render_template('index.html', clean_mass = clean_mass, glean_mass = glean_mass, goal_weight = goal_weight, 
            slow_tt6 = slow_tt6, fast_tt6 = fast_tt6, calories = calories)
        else:
            return 'Error: one or more inputs was not a number'

if __name__ == "__main__":
    app.run(debug=True)
