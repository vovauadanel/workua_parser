import csv
import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('work.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow((data['name'],
                         data['salary'],
                         data['remark'],
                         data['org'],
                         data['url']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('div', class_='card card-hover card-visited wordwrap job-link js-hot-block')

    for card in cards:
        try:
            name = card.find('h2').find('a').text.strip()
        except:
            name = ''
        try:
            salary = card.find('div', class_=None).find('b').text
        except:
            salary = ''
        try:
            salary_remarks = card.find_all('span', class_='text-muted')
            salary_remark = salary_remarks[1].text.strip()
        except:
            salary_remark = ''
        try:
            org = card.find('div', class_='add-top-xs').find('b').text
        except:
            org = ''
        try:
            url = 'https://www.work.ua/' + card.find('h2').find('a').get('href')
        except:
            url = ''

        data = {'name': name,
                'salary': salary,
                'remark': salary_remark,
                'org': org,
                'url': url}

        write_csv(data)


def main():
    f = open('work.csv', 'w')
    headers = 'Назва, Зарплата, Примітка, Організація, Посилання\n'
    f.write(headers)
    f.close()

    url = 'https://www.work.ua/jobs-kyiv/'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()
