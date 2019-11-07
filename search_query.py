import json
from datetime import datetime


class Query:
    __slots__ = ('value_query', 'site_promoted', 'url_promoted',
                 'url_result_google', 'url_result_yandex', 'position_google', 'position_yandex', )

    def __init__(self, **kwargs):
        for slot in self.__slots__:
            setattr(self, slot, kwargs.get(slot))

    def __dict__(self):
        return {slot: getattr(self, slot) for slot in self.__slots__}


class QueryList:

    def __init__(self, file):
        self.queries = self._get_queries_from_file(file)

    def __iter__(self):
        return iter(self.queries)

    def _get_queries_from_file(self, file):
        if file.endswith('.json'):
            return self._get_queries_from_json(file)
        else:
            return self._get_queries_from_txt(file)

    def _get_queries_from_txt(self, file):
        queries, url_promoted, site = [], '', ''
        for string in self._read_txt(file):
            if string.startswith('##'):
                site = string.lstrip('##')
            elif string.startswith('#'):
                url_promoted = string.lstrip('#')
            else:
                queries.append(Query(value_query=string, url_promoted=url_promoted, site_promoted=site))
        return queries

    @staticmethod
    def _read_txt(file):
        with open(file, 'r', encoding='utf-8') as read_file:
            return map(lambda line: line.rstrip(), read_file.readlines())

    def _get_queries_from_json(self, file):
        return [Query(**query) for query in self._read_json(file).get('queries')]

    @staticmethod
    def _read_json(file):
        with open(file, 'r', encoding='utf8') as read_file:
            return json.loads(read_file.read())

    def create_json(self):
        file_name = f'positions_{datetime.now(tz=None):%d_%B_%Y_%H:%M}.json'
        queries = [query.__dict__() for query in self.queries]
        with open(file_name, 'w', encoding='utf-8')as write_file:
            json.dump({'queries': queries}, write_file, sort_keys=False, indent=4, ensure_ascii=False)
