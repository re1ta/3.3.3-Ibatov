import requests
import pandas as pd


def json_convert(json):
    """
        Производит парсинг json в список значений
        Arg:
            json(dict)
    """
    salary_from,salary_to,salary_currency,area_name = None,None,None,None

    if json['salary'] is not None:
        salary_from = json['salary']['from']
        salary_to = json['salary']['to']
        salary_currency = json['salary']['currency']

    if json['area'] is not None:
        area_name = json['area']['name']

    return [json['name'], str(salary_from), str(salary_to), salary_currency, area_name, json['published_at']]


def get_vacancies():
    """
        Загружает выкансии с сайта сохраняет их в CSV
    """
    df = pd.DataFrame(columns=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at'])
    for h in range(0, 24, 6):
        url = f'https://api.hh.ru/vacancies?specialization=1&date_from=2022-12-08T{("0" + str(h))[-2:]}:00:00' \
              f'&date_to=2022-12-' \
              f'{("0" + str(8 + ((h + 6) // 24)))[-2:]}T{("0" + str((h + 6) % 24))[-2:]}:00:00'
        response = requests.get(url)

        if response.status_code != 200:
            print('Error')
            response = requests.get(url)

        result = response.json()

        for n in range(result['pages']):
            url += f'&page={n}'
            page_response = requests.get(url)

            if page_response.status_code != 200:
                print('Error')
                page_response = requests.get(url)

            for vac in page_response.json()['items']:
                df.loc[len(df.index)] = json_convert(vac)

    df.to_csv('hh.csv', index=False)


get_vacancies()