import os
import csv
import json
from collections import defaultdict
from models import AgencyBudget, FunctionSpending, ForeignAid
current_dir = os.path.dirname(os.path.abspath(__file__))


class AddGovSpending:
    def __init__(self, session):
        self.session = session
        self.add_agency_budgets()
        self.add_function_spending()
        self.add_foreign_aid()

    def add_agency_budgets(self):
        agency_file_name = os.path.join(current_dir, 'data', 'agency_resources.csv')
        with open(agency_file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                agency_budget = AgencyBudget(agency=row['Agency'], budget=row['Budget'])
                self.session.add(agency_budget)
        self.session.commit()
        print('agency budget table updated')

    def add_function_spending(self):
        for year in range(2017, 2025):
            function_file_name = os.path.join(current_dir, 'data', f'functions_{year}.csv')
            with open(function_file_name, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    function_entry = FunctionSpending(year=year, name=row['Function'], amount=row['Amount'])
                    self.session.add(function_entry)
        self.session.commit()
        print('function spending table updated')

    def add_foreign_aid(self):
        entries = self.prep_foreign_aid_data()

        self.session.query(ForeignAid).delete()

        aids = [
            ForeignAid(
                country=entry['country'],
                year=entry['year'],
                amount=entry['amount'],
                lat=entry['lat'],
                lng=entry['lng'])
            for entry in entries
        ]

        self.session.bulk_save_objects(aids)
        self.session.commit()

        print('foreign aid table updated')

    def prep_foreign_aid_data(self):
        replacements = {
            'China (Hong Kong, S.A.R., P.R.C.)': 'China',
            'China (P.R.C.)': 'China',
            'China (Tibet)': 'China',
            'Burma (Myanmar)': 'Myanmar',
            'Congo (Brazzaville)': 'Republic of the Congo',
            'Congo (Kinshasa)': 'DR Congo',
            'Korea, Democratic Republic of': 'North Korea',
            'Korea, Republic of': 'South Korea',
            'Sao Tome and Principe': 'São Tomé and Príncipe',
            'Slovak Republic': 'Slovakia',
            'Sudan (former)': 'Sudan',
            'West Bank and Gaza': 'Palestine',
            'Micronesia, Federated States of': 'Micronesia',
            'Kiribati, Republic of': 'Kiribati',
            'Curacao': 'Curaçao',
            'Serbia and Montenegro (former)': 'Serbia'
        }
        exclude = ['World']
        with open('./data/lat_lng_mapper.json', 'r') as json_file:
            lat_lng_mapper = json.load(json_file)
        data = defaultdict(lambda: defaultdict(float))
        with open('./data/foreign_aid_all.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                country = row['Country Name']
                year = row['Fiscal Year']
                amount = row['Constant Dollar Amount']
                country = replacements.get(country, country)
                try:
                    if country not in exclude and 'Region' not in country:
                        data[country][year] += int(amount)
                except Exception as e:
                    print(country, e)

        entries = []
        for country, years in data.items():
            for year, amount in years.items():
                entries.append({
                    'country': country,
                    'year': year,
                    'amount': amount,
                    'lat': lat_lng_mapper[country]['lat'],
                    'lng': lat_lng_mapper[country]['lng']
                })
        return entries
