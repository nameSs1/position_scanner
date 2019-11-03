"""
описывает класс Поисковый запрос
"""
import json
from datetime import datetime


class Query:
    query_id = 0  # id запроса

    def __init__(self, **kwargs):
        self.value_query = kwargs.get('value_query')  # Значение запросов
        self.url_promoted = kwargs.get('url_promoted')  # продвигаемая страница
        self.url_result_google = kwargs.get('url_result_google')  # URL ответа google
        self.url_result_yandex = kwargs.get('url_result_yandex')  # URL ответа yandex
        self.position_google = kwargs.get('position_google')  # позиция в google
        self.position_yandex = kwargs.get('position_yandex')  # позиция в yandex
        self.site_promoted = kwargs.get('site_promoted')  # продвигаемый сайт
        self.id = Query.query_id  # id запроса
        Query.query_id += 1

    def get_dict(self):
        dict_attrs = vars(self)
        return {dict_attrs.pop('query_id'): dict_attrs}


class QueryList:

    def __init__(self, file):
        self.queries = self._get_queries_from_file(file)

    def __iter__(self):
        return iter(self.queries)

    def _get_queries_from_file(self, file):
        if file.endswith('.json'):
            return self._read_json(file)
        else:
            return self._get_queries_from_txt(file)

    @staticmethod
    def _read_txt(file):
        with open(file, 'r', encoding='utf8') as read_file:
            return read_file.readlines()

    def _get_queries_from_txt(self, file):
        queries, url_promoted, site = [], '', ''
        for string in self._read_txt(file):
            if string.startswith('##'):
                site = string.lstrip('##').rstrip()
            elif string.startswith('#'):
                url_promoted = string.lstrip('#').rstrip()
            else:
                queries.append(Query(value_query=string.rstrip(), url_promoted=url_promoted, site_promoted=site))
        return queries

    @staticmethod
    def _read_json(file):
        with open(file, 'r', encoding='utf8') as read_file:
            return json.loads(read_file.read())

    def _get_queries_from_json(self, file):
        queries = []
        for element in self._read_json(file).get('queries'):
            queries.append(Query())
            for attr in element:
                setattr(queries[-1], attr, element.get(attr))
        return queries

    def create_json(self):
        file_name = f'positions_{datetime.now(tz=None):%d_%B_%Y_%H:%M}.json'
        queries = [vars(query) for query in self.queries]
        with open(file_name, 'w', encoding='utf-8')as write_file:
            json.dump({'queries': queries}, write_file, sort_keys=False, indent=4, ensure_ascii=False)
