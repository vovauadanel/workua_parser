import csv
import requests
from bs4 import BeautifulSoup
import time

start_time = time.time()


def get_html(url):
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0'}
    r = requests.get(url, headers=user_agent)
    if r.ok:
        return r.text
    print(r.status_code)


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
        name = card.find('h2').find('a').text.strip()
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


def get_page_data_65(html):
    '''Func is called after page 65 (div changes)'''
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('div', class_='card card-hover card-visited wordwrap job-link')  # div has no 'js-hot-block' in the end

    for card in cards:
        name = card.find('h2').find('a').text.strip()
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
    with open('work.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('Назва', 'Зарплата', 'Примітка', 'Організація', 'Посилання'))

    url = 'https://www.work.ua/jobs-kyiv/'
    x = 1  # counter of pages
    print(f'Обробка {x} сторінки')
    while True:
        if x < 65:
            get_page_data(get_html(url))
        elif x > 65:
            get_page_data_65(get_html(url))
        soup = BeautifulSoup(get_html(url), 'lxml')

        try:
            url = 'https://www.work.ua' + soup.find('div', id='pjax-job-list').find('nav').\
                  find('ul', class_='pagination hidden-xs').find_all('li')[-1].find('a').get('href')
            print(url)
            x += 1
            print(f'Обробка {x} сторінки')
        except:
            print(f'Оброблено {x} сторінок')
            print(f'Затрачено {time.time() - start_time}')
            break


if __name__ == '__main__':
    main()
