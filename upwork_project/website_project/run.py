from flask import Flask, render_template, request
from website_project.models.dashboard_model import Dashboard
import os

app = Flask(__name__)


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

    month = request.args.get('month')
    name = request.args.get('station_name')
    price = request.args.get('price')
    static_path = os.path.join("static", 'images', "keypiechart.png")

    dashboard_obj = Dashboard(month, name, price)
    energy_sum, energy_avg, session_count, duration_avg, cost_total \
        = dashboard_obj.numeric_data()
    dashboard_obj.key_chart()

    return render_template("index.html", names=charging_station_names,
                           months=months, energy_total=energy_sum,
                           session_number=session_count,
                           duration_avg=duration_avg,
                           energy_avg=energy_avg, cost_total=cost_total,
                           path=static_path)


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
