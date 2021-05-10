from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    weight = db.Column(db.Float, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        weight = request.form['weight']
        cbodyfat = request.form['cbodyfat']
        gbodyfat = request.form['gbodyfat']

        new_weight = Data(weight = weight)
        try:
            db.session.add(new_weight)
            db.session.commit()

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
                weights = Data.query.order_by(Data.date_created.desc()).all()
                return render_template('index.html', clean_mass = clean_mass, glean_mass = glean_mass, goal_weight = goal_weight, 
                slow_tt6 = slow_tt6, fast_tt6 = fast_tt6, calories = calories, weights = weights)
            else:
                return 'Error: one or more inputs was not a number'
        except:
            return 'Error: could not add weight'
    else:
        weights = Data.query.order_by(Data.date_created.desc()).all()
        return render_template('index.html', weights = weights)

#form submission
@app.route('/delete/<int:id>')
def delete(id):
    weight_to_delete = Data.query.get_or_404(id)

    try:
        db.session.delete(weight_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that weight'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    weight = Data.query.get_or_404(id)

    if request.method == 'POST':
        weight.weight = request.form['weight']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your weight'
    else:
        return render_template('update.html', weight=weight)

@app.route('/hello')
def hello():
    return 'Hello'

if __name__ == "__main__":
    app.run(debug=True)