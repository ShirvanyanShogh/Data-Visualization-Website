import os
import pandas as pd
from datetime import datetime, timedelta


class Dashboard:
    def __init__(self, month, year, name, price):
        self.month = month
        self.year = year
        self.price = price
        self.ok = False
        if month:
            fname = ''.join([name.replace(" ", "-"), "-", month, ".csv"])
            datafiles_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "datafiles")
            for filename in os.listdir(datafiles_path):
                if filename.lower() == fname.lower():
                    print(filename)
                    # if fname in os.listdir(datafiles_path):
                    self.ok = True
                    self.df = pd.read_csv(os.path.join(datafiles_path,filename))
                    self.df['energy'] = \
                        pd.to_numeric(self.df['energy'].str.replace(',', '.'))

    def numeric_data(self):
        energy_sum = 0
        energy_avg = 0
        session_count = 0
        duration_avg = 0
        cost_total = 0
        if self.ok:
            energy_total = self.df['energy'].sum()
            energy_sum = f"{energy_total:.2f}"
            energy_avg = f"{self.df['energy'].mean():.2f}"
            session_count = self.df['sessionId'].count()
            duration_avg = (pd.to_timedelta(self.df['duration']).mean()). \
                floor('s')
            if duration_avg.days == 0:
                duration_avg = str(duration_avg).split()[2]

            cost_total = f"{(energy_total * float(self.price)):.2f}"

        return energy_sum, energy_avg, session_count, duration_avg, cost_total

    def pie_chart(self):
        energy_per_key = {}
        energy_per_user = {}
        energy_per_connector = {}
        energy_per_day = {}
        if self.ok:
            energy_per_key = \
                dict(self.df.groupby(self.df['keyIdentifier']).sum()['energy'])
            energy_per_user = \
                dict(self.df.groupby(self.df['userId']).sum()['energy'])
            energy_per_connector = \
                dict(self.df.groupby(self.df['connectorId']).sum()['energy'])

        return energy_per_key, energy_per_user, energy_per_connector

    def energy_per_day(self):
        energy_per_day = {}
        if self.ok:
            start_date = pd.to_datetime(self.df['startTime'])
            energy_per_day_partial = \
                self.df.groupby(start_date.dt.date).sum()['energy']

            month_number = datetime.strptime(self.month[0:3], "%b").month
            if month_number == 2 and int(self.year) % 4 == 0:
                month_days = 29
            elif month_number == 2 and int(self.year) % 4 != 0:
                month_days = 28
            elif month_number in (1, 3, 5, 7, 8, 10, 12):
                month_days = 30
            elif month_number in (4, 6, 9, 11):
                month_days = 31

            start_date = f"{int(self.year)}-{month_number}-01"  # ex. 2020-01-01
            data = pd.date_range(start=start_date, periods=month_days).date
            month_empty_data = pd.Series(0, data)
            energy_per_day = dict(
                ((energy_per_day_partial + month_empty_data).fillna(0)))

        return energy_per_day

    def energy_usage(self):
        ranges = {'00:00-02:00': timedelta(0), '02:00-04:00': timedelta(0),
                  '04:00-06:00': timedelta(0), '06:00-08:00': timedelta(0),
                  '08:00-10:00': timedelta(0), '10:00-12:00': timedelta(0),
                  '12:00-14:00': timedelta(0), '14:00-16:00': timedelta(0),
                  '16:00-18:00': timedelta(0), '18:00-20:00': timedelta(0),
                  '20:00-22:00': timedelta(0), '22:00-00:00': timedelta(0)}
        if self.ok:
            self.df['startTime'] = pd.to_datetime(self.df['startTime'])
            self.df['duration'] = pd.to_timedelta(self.df['duration'])
            for ind in self.df.index:
                start_time = self.df['startTime'][ind]
                duration = self.df['duration'][ind]
                h = start_time.hour
                if h % 2 != 0:
                    time = (start_time + timedelta(hours=1)).replace(minute=00,
                                                                     second=00)
                elif h % 2 == 0:
                    time = (start_time + timedelta(hours=2)).replace(minute=00,
                                                                     second=00)
                accumulated_hours = timedelta(0)
                while time - start_time < duration:
                    variance = time - start_time - accumulated_hours
                    accumulated_hours = accumulated_hours + variance
                    range_str = self.usage_support(time)
                    ranges[range_str] = ranges[range_str] + variance
                    time = (time + timedelta(hours=2)).replace(minute=00,
                                                               second=00)

                if time - start_time >= duration:
                    range_str = self.usage_support(time)
                    ranges[range_str] = ranges[
                                            range_str] + duration - accumulated_hours

            for key, value in ranges.items():
                hours = value.seconds / 60 / 60 + value.days * 24
                ranges[key] = f"{hours:.2f}"

        return ranges

    @staticmethod
    def usage_support(time):
        range_start = (time - timedelta(hours=2)).replace(minute=00,
                                                          second=00)
        range_start = str(range_start).split(' ')[1][0:5]
        range_end = str(time).split(' ')[1][0:5]
        range_str = f"{range_start}-{range_end}"

        return range_str


# obj = Dashboard("February", 2020, "Eli Lilly LI CP1 002", "0.18")
# # print(obj.numeric_data())
# # print(obj.pie_chart())
# # print(obj.energy_usage())
