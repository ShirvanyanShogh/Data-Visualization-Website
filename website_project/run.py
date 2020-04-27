from flask import Flask, render_template, request, flash, redirect, url_for
from website_project.models.dashboard_model import Dashboard
from website_project.models.forms import RegistrationForm, LoginForm
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "2f546fa116533c013fceb653c20ef64f"


@app.route('/')
def dashboard():
    charging_station_names = ["Rockgrove CP1 001", "Marymount CP1 001",
                              "Marymount CP1 002", "Eli Lilly LI CP1 001",
                              "Eli Lilly LI CP1 002", "Eli Lilly LI CP1 003",
                              "Shanahan Circle K CP1 001", "Hovione CP1 001",
                              "Hovione CP1 002", "Hovione CP1 003",
                              "Hovione CP1 004", "Crest CP1 001"]

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    years = [2018, 2019, 2020]

    month = request.args.get('month')
    name = request.args.get('station_name')
    year = request.args.get('year')
    price = request.args.get('price')
    static_path = os.path.join("static", 'images', "keypiechart.png")

    dashboard_obj = Dashboard(month, name, price)
    energy_sum, energy_avg, session_count, duration_avg, cost_total \
        = dashboard_obj.numeric_data()
    energy_per_key, energy_per_user, energy_per_connector, energy_per_day \
        = dashboard_obj.pie_chart()

    return render_template("index.html", names=charging_station_names,
                           months=months, years=years, energy_total=energy_sum,
                           session_number=session_count,
                           duration_avg=duration_avg,
                           energy_avg=energy_avg, cost_total=cost_total,
                           path=static_path, energy_per_key=energy_per_key,
                           energy_per_day=energy_per_day,
                           energy_per_user=energy_per_user,
                           energy_per_connector=energy_per_connector)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("You have been logged in!", 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html', title="Login", form=form)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
