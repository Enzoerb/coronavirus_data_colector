import requests
from requests_html import HTML
import sys
import csv
from datetime import datetime
import os


class Corona_Info:

    def __init__(self):
        self.date = datetime.now().strftime('%Y/%m/%d %H:%M')
        self.cases = 0
        self.deaths = 0
        self.recoveries = 0

    @property
    def location(self):
        if len(sys.argv) == 2:
            return sys.argv[1].lower()
        return 'world'

    @property
    def site_link(self):
        link = 'https://www.worldometers.info/coronavirus/'
        if self.location != 'world':
            return link + f'country/{self.location}'
        return link

    def get_html(self):
        r = requests.get(self.site_link)
        source = r.text
        html = HTML(html=source)
        return html

    def update_cases(self, html):
        match = html.find('#maincounter-wrap')
        cases_info = (match[0].text).split('\n')
        cases_info[1] = int(cases_info[1].replace(',', ''))
        self.cases = cases_info[1]

    def update_deaths(self, html):
        match = html.find('#maincounter-wrap')
        deaths_info = (match[1].text).split('\n')
        deaths_info[1] = int(deaths_info[1].replace(',', ''))
        self.deaths = deaths_info[1]

    def update_recoveries(self, html):
        match = html.find('#maincounter-wrap')
        recoveries_info = (match[2].text).split('\n')
        recoveries_info[1] = int(recoveries_info[1].replace(',', ''))
        self.recoveries = recoveries_info[1]

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
    Info = Corona_Info()
    html = Info.get_html()
    Info.update_cases(html)
    Info.update_deaths(html)
    Info.update_recoveries(html)
    local_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(local_path, 'corona.csv')
    Info.to_csv(csv_path)
    print(f'{Info.cases};{Info.deaths};{Info.recoveries}')
