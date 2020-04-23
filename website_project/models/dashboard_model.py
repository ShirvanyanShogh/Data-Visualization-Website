import os
import pandas as pd
import matplotlib.pyplot as plt
from decimal import Decimal


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
            print(self.df)
            energy_total = self.df['energy'].sum()
            energy_sum = f"{round(energy_total):,}"
            energy_avg = f"{round(self.df['energy'].mean()):,}"
            session_count = self.df['sessionId'].count()
            duration_avg = pd.to_timedelta(self.df['duration']).mean()
            duration_avg = str(duration_avg)[7:]
            cost_total = energy_total * Decimal(self.price)

        return energy_sum, energy_avg, session_count, duration_avg, cost_total

    def key_chart(self):
        if self.ok:
            keyid_enerygy = \
                dict(self.df.groupby(self.df['keyIdentifier']).sum()['energy'])
            labels = list(keyid_enerygy.keys())
            sizes = list(keyid_enerygy.values())
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
            plt.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%',
                     startangle=90, pctdistance=0.85)
            centre_circle = plt.Circle((0, 0), 0.70, fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            plt.tight_layout()
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                "static", 'images', "keypiechart.png")
            # os.remove(path)
            plt.savefig(path)

