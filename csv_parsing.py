import pandas as pd

pd.set_option("display.max_columns", False)
pd.set_option("expand_frame_repr", False)


def parse_csv_by_year(file="vacancies_by_year.csv"):
    """
        Группирует данные во входном файле по годам
        Arg:
            file(str) : Название файла
    """
    csv_file = pd.read_csv(file)
    csv_file["year"] = csv_file["published_at"].apply(lambda s: s[:4])
    df = csv_file.groupby("year")
    for year, data in df:
        data[[
            "name", "salary_from", "salary_to",
            "salary_currency", "area_name", "published_at"]]\
            .to_csv(rf"years\year_{year}.csv", index=False)


parse_csv_by_year()
