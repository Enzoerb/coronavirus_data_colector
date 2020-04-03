import requests
import re
import sys
import csv
from datetime import datetime
import os


class Corona_Info:

    def __init__(self, location):
        self.date = datetime.now().strftime('%Y/%m/%d %H:%M')
        self.location = location
        self.cases = 0
        self.deaths = 0
        self.recoveries = 0

    @property
    def site_link(self):
        link = 'https://www.worldometers.info/coronavirus/'
        if self.location != 'world':
            return link + f'country/{self.location}'
        return link

    def get_html(self):
        r = requests.get(self.site_link)
        source = r.text
        return source

    def update_cases(self, html):
        pattern = re.compile(
            r'<h1>(Coronavirus Cases:)</h1>\s<div(\s[=\w]+\W[-:#\s\w]+\W)+>\s<span>?\s?([=\w]+\W[-:#\w]+\W>)?([\d,]+)\s?</span>')
        query = pattern.search(html)
        number_cases = query.group(4)
        self.cases = int(number_cases.replace(',', ''))

    def update_deaths(self, html):
        pattern = re.compile(
            r'<h1>(Deaths:)</h1>\s<div(\s[=\w]+\W[-:#\s\w]+\W)+>\s<span>?\s?([=\w]+\W[-:#\w]+\W>)?([\d,]+)\s?</span>')
        query = pattern.search(html)
        number_deaths = query.group(4)
        self.deaths = int(number_deaths.replace(',', ''))

    def update_recoveries(self, html):
        pattern = re.compile(
            r'<h1>(Recovered:)</h1>\s<div(\s[=\w]+\W[-:#\s\w]+\W)+>\s<span>?\s?([=\w]+\W[-:#\w]+\W>)?([\d,]+)\s?</span>')
        query = pattern.search(html)
        number_recoveries = query.group(4)
        self.recoveries = int(number_recoveries.replace(',', ''))

    def to_csv(self, file_name):
        if not os.path.exists(file_name):
            with open(file_name, 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['date', 'location', 'cases', 'deaths', 'recoveries'])

        with open(file_name, 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([f'{self.date}',
                                 f'{self.location.title()}',
                                 f'{self.cases}',
                                 f'{self.deaths}',
                                 f'{self.recoveries}'])


if __name__ == '__main__':
    location = sys.argv[1].lower() if len(sys.argv) == 2 else 'world'
    Info = Corona_Info(location)

    html = Info.get_html()
    Info.update_cases(html)
    Info.update_deaths(html)
    Info.update_recoveries(html)

    local_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(local_path, 'csv_data')):
        os.mkdir('csv_data')

    csv_path = os.path.join(local_path, 'csv_data/corona.csv')
    location_csv_path = os.path.join(local_path, f'csv_data/corona_{location}.csv')
    Info.to_csv(csv_path)
    Info.to_csv(location_csv_path)
    if sys.stdin.isatty():
        print(f'{Info.cases};{Info.deaths};{Info.recoveries}')
