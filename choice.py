import table
import statistic

"""
    Запускает функцию выбора формата вывода данных (таблица в консоли или таблица эклесь, pdf и фото)
    Возращает таблицу в консоли, либо таблицу эксель, пдф и фото 
"""
def start():
    a = input("Требуемый формат данных: ")
    if a == "Вакансии": table.get_table()
    elif a == "Статистика": statistic.get_statistic()
    else: print("Неккоректный ввод")

start()