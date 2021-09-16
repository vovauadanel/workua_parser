import csv
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
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


def make_all(url):
    text = get_html(url)
    get_page_data(text)


def make_all_65(url):
    text = get_html(url)
    get_page_data_65(text)


def main():
    with open('work.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('Назва', 'Зарплата', 'Примітка', 'Організація', 'Посилання'))

    url = 'https://www.work.ua/jobs-kyiv/?page={}'
    urls = [url.format(str(i)) for i in range(1, 2790)]



    with Pool(2) as p:
        p.map(make_all, urls[:65])
        p.map(make_all_65, urls[65:])


    print(f'Затрачено {time.time() - start_time}')


if __name__ == '__main__':
    main()
