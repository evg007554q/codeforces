import requests
from configparser import ParsingError

from func import db_manager


def parsing_code():

    db = db_manager.DBManager()


    response = requests.get("https://codeforces.com/api/problemset.problems").json()

    # if response.status_code != 200:
    #     raise ParsingError(f'Ошибка подключения к codeforces.ru! Статус:{response.status_code}')

    Problems = response["result"]["problems"]
    ProblemStatistics = response["result"]["problemStatistics"]

    #обновляем в базе задачи
    for Problem in Problems:

        if 'rating' in Problem:
            rating = Problem['rating']
        else:
            rating = 0
        url = f"https://codeforces.com/problemset/problem/{Problem['contestId']}/{Problem['index']}"

        db.db_update_Problem(Problem['contestId'], Problem['index'], Problem['name'], url, rating, Problem["tags"])



    #добавляем в базу задачи
    for Problem in Problems:

        if 'rating' in Problem:
            rating = Problem['rating']
        else:
            rating = 0
        url = f"https://codeforces.com/problemset/problem/{Problem['contestId']}/{Problem['index']}"

        db.db_add_Problem(Problem['contestId'], Problem['index'], Problem['name'], url, rating, Problem["tags"])

        for tag in Problem["tags"]:
            db.db_add_tag(Problem['contestId'], Problem['index'], tag )

        # break

    #обновляем задачи
    for ps in ProblemStatistics:
        db.db_add_Problem_solvedCount(ps['contestId'], ps['index'], ps['solvedCount'])


