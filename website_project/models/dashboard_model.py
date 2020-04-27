import os
import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal
import numpy as np


class Dashboard:
    def __init__(self, month, name, price):
        self.month = month
        self.price = price
        self.ok = False
        if month:
            fname = ''.join([name.replace(" ", "-"), "-", month, ".csv"])
            datafiles_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "datafiles")
            if fname in os.listdir(datafiles_path):
                self.ok = True
                self.df = pd.read_csv(os.path.join(datafiles_path, fname))
                self.df['energy'] = \
                    self.df['energy'].str.replace(',', '').astype(int)

    def numeric_data(self):
        energy_sum = 0
        energy_avg = 0
        session_count = 0
        duration_avg = 0
        cost_total = 0
        if self.ok:
            energy_total = self.df['energy'].sum()
            energy_sum = f"{round(energy_total):,}"
            energy_avg = f"{round(self.df['energy'].mean()):,}"
            session_count = self.df['sessionId'].count()
            duration_avg = (pd.to_timedelta(self.df['duration']).mean()).\
                floor('s')
            if duration_avg.days == 0:
                duration_avg = str(duration_avg).split()[2]

            cost_total = energy_total * Decimal(self.price)

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
            start_date = pd.to_datetime(self.df['startTime'])
            # energy_per_day = dict(self.df.groupby(start_date.dt.floor("d")).sum()['energy'])
            energy_per_day = dict(self.df.groupby(start_date.dt.floor("d").
                                                  dt.date).sum()['energy'])

        return energy_per_key, energy_per_user, energy_per_connector, \
               energy_per_day


obj=Dashboard("February", "Eli Lilly LI CP1 002", "0.18")
print(obj.numeric_data())
