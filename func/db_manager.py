import psycopg2
from psycopg2 import DatabaseError
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


class DBManager:
    # print(os.getenv('DB_NAME'))
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME')
            ,user=os.getenv('DB_USER')
            ,host=os.getenv('DB_HOST')
            ,password=os.getenv('DB_PASSWORD')
        )
        self.conn.autocommit = True

    def qw(self, queries_text):
        try:
            with self.conn.cursor() as cur:
                cur.execute(queries_text)
                return cur.fetchall()
        except DatabaseError as e:
            print(e)
            raise DatabaseError


    def db_add_Problem(self, contestId, index, name, url, rating, tags):
        id=str(contestId)+index
        # print(tags)
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
              cur.execute(f"INSERT INTO public.problem(id_problem, name, contestId, index, url, rating, tags) "
                          f"select %s, %s, %s, %s, %s, %s, %s where not exists (select id_problem from problem where id_problem='{id}')"
                          ,
                          (id,name,contestId,index,url,rating,tags))


        return None

    def db_update_Problem(self, contestId, index, name, url, rating, tags):
        id=str(contestId)+index
        # print(tags)
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
              cur.execute(f"UPDATE public.problem "
                          f"SET  name=%s, rating=%s, tags=%s where id_problem='{id}'"
                          ,
                          (name,rating,tags))


        return None
    def db_add_tag(self, contestId, index, tag):
        id=str(contestId)+index
        # print(tags)
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
              cur.execute(f"INSERT INTO public.problem_tags(id_problem, tag) "
                          f"select %s, %s where not exists (select id_problem from problem_tags where id_problem='{id}' and tag='{tag}')"
                          ,
                          (id,tag))


        return None


    def db_add_Problem_solvedCount(self, contestId, index, solvedCount):
        id=str(contestId)+index

        self.conn.autocommit = True
        with self.conn.cursor() as cur:
              cur.execute(f"UPDATE public.problem "
                          f"SET solvedCount = %s where id_problem='{id}'"
                          ,
                          (solvedCount,))


        return None




    #
    # def get_companies_and_vacancies_count(self):
    #     # - get_companies_and_vacancies_count(): получает список всех компаний и количество вакансий у каждой компании.
    #     return self.qw(select_employers())


