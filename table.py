import csv
import re
from datetime import datetime

class Vacancy:
    """
        Класс инициализирует название, зарплату, название региона, дату публикции вакансий
        Attributes
        ----------
        name(str) : Название вакансии
        salary(str) : Зарплата вакансии
        area_name(str) : Название региона вакансии
        published_at(str) : Дата публикции вакансии
    """
    def __init__(self, name, salary, area_name, published_at):
        """
            Метод инициализирует название, зарплату, название региона, дату публикции вакансий
            Arg:
                name(str) : Название вакансии
                salary(str) : Зарплата вакансии
                area_name(str) : Название региона вакансии
                published_at(str) : Дата публикции вакансии
        """
        self.name = name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at

class Salary:
    """
        Класс инициализирует нижнюю, верхнюю границу вилки оклада и валюту,
        а также переводит иностранную валюту в рубли
        Attributes
        ----------
        salary_from (str) : Нижняя граница вилки оклада
        salary_to(str) : Верхняя граница вилки оклада
        salary_currency(str) : Валюта
    """
    def __init__(self, salary_from, salary_to, salary_currency):
        """
            Метод инициализирует нижнюю, верхнюю границу вилки оклада и валюту
            Arg:
                salary_from (str) : Нижняя граница вилки оклада
                salary_to(str) : Верхняя граница вилки оклада
                salary_currency(str) : Валюта
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency

    def get_salary_in_rub(self):
        """
            Метод переводит иностранную валюту в рубли
        """
        return ((int(float(self.salary_from)) + int(float(self.salary_to))) / 2) * currency_to_rub[self.salary_currency]

class InputConect:
    """
        Класс ввода и вывода
        Attributes
        ----------
        file_name (str) : Название файла
        vac_name (str) : Название профессии
    """
    def make(self):
        """
            Метод ввода файла и профессии
        """
        file_name = input('Введите название файла: ')
        vac_name = input('Введите название профессии: ')
        data_set = DataSet(file_name)
        InputConect.printing_data_for_table(data_set, vac_name)

    @staticmethod
    def printing_data_for_table(dataset, vac_name):
        """
            Метод образует данные в таблицу и выводит их
            Arg:
                dataset (list) : Массив вакансий
                vac_name (str) : Название профессии
        """
        dic_vacancies = dataset.vacancies_objects
        years = set()
        for vacancie in dic_vacancies:
            years.add(int(datetime.strptime(vacancie.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime("%Y")))
        years = sorted(list(years))
        years = list(range(min(years), max(years) + 1))

        years_salary_dic = {year: [] for year in years}
        years_count_dic = {year: 0 for year in years}
        years_salary_vac_dic = {year: [] for year in years}
        years_count_vac_dic = {year: 0 for year in years}

        for vacancie in dic_vacancies:
            y = int(datetime.strptime(vacancie.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime("%Y"))
            years_salary_dic[y].append(vacancie.salary.get_salary_in_rub())
            years_count_dic[y] += 1
            if vac_name in vacancie.name:
                years_salary_vac_dic[y].append(vacancie.salary.get_salary_in_rub())
                years_count_vac_dic[y] += 1

        years_salary_dic = {key: int(sum(value) / len(value)) if len(value) != 0 else 0 for key, value in years_salary_dic.items()}
        years_salary_vac_dic = {key: int(sum(value) / len(value)) if len(value) != 0 else 0 for key, value in years_salary_vac_dic.items()}

        area_dic = {}
        for vacancie in dic_vacancies:
            if vacancie.area_name in area_dic:
                area_dic[vacancie.area_name].append(vacancie.salary.get_salary_in_rub())
            else:
                area_dic[vacancie.area_name] = [vacancie.salary.get_salary_in_rub()]

        area_list = area_dic.items()
        area_list = [x for x in area_list if len(x[1]) >= int(len(dic_vacancies) / 100)]
        area_list = sorted(area_list, key=lambda item: sum(item[1]) / len(item[1]), reverse=True)
        area_salary_dic = {item[0]: int(sum(item[1]) / len(item[1])) for item in area_list[0: min(len(area_list), 10)]}
        area_list = sorted(area_list, key=lambda item: len(item[1]) / len(dic_vacancies), reverse=True)
        area_count_dic = {item[0]: round(len(item[1]) / len(dic_vacancies), 4) for item in area_list[0: min(len(area_list), 10)]}

        print("Динамика уровня зарплат по годам: " + str(years_salary_dic))
        print("Динамика количества вакансий по годам: " + str(years_count_dic))
        print("Динамика уровня зарплат по годам для выбранной профессии: " + str(years_salary_vac_dic))
        print("Динамика количества вакансий по годам для выбранной профессии: " + str(years_count_vac_dic))
        print("Уровень зарплат по городам (в порядке убывания): " + str(area_salary_dic))
        print("Доля вакансий по городам (в порядке убывания): " + str(area_count_dic))

class DataSet:
    """
        Класс обработки чтения и обработки csv-файла
        Attributes
        ----------
        file_name (str) : Название файла
        vacancies_objects (list) : Массив вакансий
    """
    def __init__(self, file_name):
        """
            Метод инициализирует назвние файла и массив вакансий
            Arg:
                file_name(str) : Название файла
        """
        self.file_name = file_name
        self.vacancies_objects = DataSet.parser_csv(file_name)

    @staticmethod
    def clear_str(str_value):
        """
            Метод чистит текст от html-тегов
            Arg:
                str_value(str) : текст в ичейках массива вакансий
        """
        return ' '.join(re.sub(r"<[^>]+>", '', str_value).split())

    @staticmethod
    def csv_reader(file_name):
        """
            Метод читает csv-файл
            Arg:
                file_name(str) : Название файла
        """
        file = open(file_name, encoding='utf_8_sig')
        reader = [row for row in csv.reader(file)]
        try:
            name = reader.pop(0)
            return name, reader
        except:
            print('Пустой файл')
            exit()

    @staticmethod
    def parser_csv(file_name):
        """
            Метод парсит csv-файл
            Arg:
                file_name(str) : Название файла
        """
        naming, reader = DataSet.csv_reader(file_name)
        dic_vacancies = []
        filtered_vacancies = [x for x in reader if len(x) == len(naming) and '' not in x]
        for row in filtered_vacancies:
            dic = {}
            for i in range(0, len(row)):
                if row[i].find("\n") != -1:
                    ans = [DataSet.clear_str(el) for el in row[i].split('\n')]
                else:
                    ans = DataSet.clear_str(row[i])
                dic[naming[i]] = ans
            dic_vacancies.append(
                Vacancy(dic['name'], Salary(dic['salary_from'], dic['salary_to'], dic['salary_currency']),
                        dic['area_name'], dic['published_at']))
        return dic_vacancies
"""
    Словарь перевода имён параметров вакансий
"""
dic_naming = {
    'name': 'Название',
    'description': 'Описание',
    'key_skills': 'Навыки',
    'experience_id': 'Опыт работы',
    'premium': 'Премиум-вакансия',
    'employer_name': 'Компания',
    'salary_from': 'Нижняя граница вилки оклада',
    'salary_to': 'Верхняя граница вилки оклада',
    'salary_gross': 'Оклад указан до вычета налогов',
    'salary_currency': 'Идентификатор валюты оклада',
    'area_name': 'Название региона',
    'published_at': 'Дата публикации вакансии'
}
"""
    Словарь перевода опыта работы
"""
experience = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет"
}
"""
    Словарь перевода валюты оклады
"""
currency = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
}
"""
    Словарь перевода иностранной валюты к рублю
"""
currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}
"""
    Словарь перевода текстового опыта работы к числам
"""
experience_convert = {
    "noExperience": 0,
    "between1And3": 1,
    "between3And6": 2,
    "moreThan6": 3
}
"""
    Словарь перевода для "Да" и "Нет"
"""
true_false = {
    'False': 'Нет',
    'True': 'Да'
}


def reverse_dic(dic):
    """
        Метод переворачивает словарь вакансий
        Arg:
            dic(dict) : Словарь вакансий
    """
    return {value: key for key, value in dic.items()}


dic_naming_reverse = reverse_dic(dic_naming)
experience_reverse = reverse_dic(experience)
currency_reverse = reverse_dic(currency)
true_false_reverse = reverse_dic(true_false)


def get_table():
    """
        Метод выводит статистику в таблицу
    """
    a = InputConect()
    a.make()