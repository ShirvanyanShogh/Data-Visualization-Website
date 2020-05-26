from flask import Flask, render_template, request, flash, redirect, url_for, session
from models.dashboard_model import Dashboard
from models.forms import RegistrationForm, LoginForm
from models.user_model import User

app = Flask(__name__)
app.config["SECRET_KEY"] = '966e27e8d5eb01266f43dc96f8a9d812'


@app.route('/')
def dashboard():
    if "email" in session:

        charging_station_names = User.get_access(session.get('email'))
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November',
                  'December']
        years = [2018, 2019, 2020]

        month = request.args.get('month')
        name = request.args.get('station_name')
        year = request.args.get('year')
        price = request.args.get('price')

        dashboard_obj = Dashboard(month, year, name, price)
        energy_sum, energy_avg, session_count, duration_avg, cost_total \
            = dashboard_obj.numeric_data()
        energy_per_key, energy_per_user, energy_per_connector \
            = dashboard_obj.pie_chart()
        energy_per_day = dashboard_obj.energy_per_day()
        energy_usage = dashboard_obj.energy_usage()

        return render_template("index.html", names=charging_station_names,
                               months=months, years=years,
                               energy_total=energy_sum,
                               session_number=session_count,
                               duration_avg=duration_avg,
                               energy_avg=energy_avg, cost_total=cost_total,
                               energy_per_key=energy_per_key,
                               energy_per_day=energy_per_day,
                               energy_per_user=energy_per_user,
                               energy_per_connector=energy_per_connector,
                               energy_usage=energy_usage)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "email" in session:
        return redirect((url_for('dashboard')))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.check_user_password(email, password)
        if user:
            session['email'] = email
            session.permanent = form.remember.data
            # flash("You have been logged in!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Login Unsuccessful. Please check email and password",
                  'danger')
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
