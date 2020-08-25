import requests
import concurrent
import time
import concurrent.futures

from sqlite3worker import Sqlite3Worker


class RequestVacancy(object):
    def __init__(self, URL):
        self.URL = URL

    def request_items(self, page):
        _vacancy_id_list = []
        _par = {'text': self.vacancy_name, 'area': self.area, 'per_page': '100', 'page': page}
        try:
            _vacancy_description_list = requests.get(self.URL, params=_par).json()['items']
        except KeyError as exception_:
            print(exception_)
            return
        for _vacancy_description in _vacancy_description_list:
            _vacancy_id_list.append(self.URL + _vacancy_description['id'])
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
            pool.map(self.request_vacancy_id, _vacancy_id_list)

    def request_vacancy_id(self, vacancy_url):
        try:
            _vacancy = requests.get(vacancy_url)
            assert (_vacancy.status_code == 200), ("Ошибка, Код ответа: ", _vacancy.status_code, vacancy_url)
        except Exception as exception_:
            print(exception_)
            time.sleep(5)
            return self.request_vacancy_id(vacancy_url)
        else:
            _key_skills_string = ''
            _vacancy = _vacancy.json()
            for _key_skill in _vacancy['key_skills']:
                _skill = _key_skill['name']
                if _skill is not None:
                    _key_skills_string += _skill + ', '
            if len(_key_skills_string) > 0:
                _key_skills_string = _key_skills_string[:-2]
            self.connect_.execute("INSERT INTO Result (id,name,area,employer,keySkills) VALUES (?,?,?,?,?)",
                                  (_vacancy['id'], _vacancy['name'],
                                   _vacancy['area']['name'],
                                   _vacancy['employer']['name'],
                                   _key_skills_string))

    def request(self, vacancy_name, area):
        self.vacancy_name = vacancy_name
        self.area = area

        self.connect_ = Sqlite3Worker(r'Result.db')
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            pool.map(self.request_items, range(20))
        self.connect_.close()
