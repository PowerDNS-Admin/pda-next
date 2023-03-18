import re
from django.db.models import Model, Q, QuerySet
from django.http import HttpResponse, QueryDict
from lib.mutables import Mutable


class SearchException(Exception):
    """ Exception for Search API """


class SearchConfigException(Exception):
    """ Exception for SearchConfig """


class SearchColumn(Mutable):
    """ SearchColumn Properties """

    SORT_ASC: str = 'asc'
    SORT_DESC: str = 'desc'
    name: str | None = None
    searchable: bool = True
    orderable: bool = True
    query: str | None = None
    global_search: bool = True
    case_sensitive: bool = False
    default_sort: str | None = None


class SearchConfig(Mutable):
    """ SearchConfig Properties """

    _key_pattern: str = r'^(columns|order)\[([\d]+)\](?:\[([\w\-\.]+)\])(?:\[([\w\-\.]+)\])?'
    _columns: dict[str, SearchColumn] | None = None
    _column_order: list[str] | None = None
    _sort_order: dict[int, tuple[SearchColumn, str]] | None = None
    _sort: tuple[str, str] | None = None
    _start: int = 0
    _limit: int = 10
    _query: str | None = None
    _filters: dict[str, str] | None = None
    _request_query: QueryDict | None = None
    _var_start: str = 'start'
    _var_limit: str = 'length'
    _var_query: str = 'search[value]'
    _request_params_loaded: bool = False

    @property
    def columns(self) -> dict[str, SearchColumn] | None:
        """ Return the columns dict. """
        return self._columns

    @columns.setter
    def columns(self, value: dict[str, SearchColumn] | list | None):
        """ Set the columns. If the columns are not a dict or list, a SearchConfigException exception will be raised.
        """
        if isinstance(value, dict):
            self._columns = value
            self._column_order = list(value.keys())
        elif isinstance(value, list):
            self._columns = {}
            self._column_order = value
            for name in list[str](value):
                self.add_column(name.lstrip('-'))
        else:
            raise SearchConfigException('Columns must be a dict[str, SearchColumn].')

        self._load_request_params()

    @property
    def column_order(self) -> list[str] | None:
        """ Return the column order list. """
        return self._column_order

    @property
    def sort_order(self) -> dict[int, tuple[SearchColumn, str]] | None:
        """ Return the sort order dict. """
        return self._sort_order

    @property
    def sortables(self) -> list[str] | None:
        """ Return a list of sortable column names. """
        if not isinstance(self._column_order, list):
            return None

        return [el for el in self._column_order if not el.startswith('-')]

    @property
    def sort(self) -> tuple[str, str] | None:
        """ Return the sort tuple. """
        return self._sort

    @sort.setter
    def sort(self, value: tuple[str, str] | None):
        """ Set the sort. If the sort is not a tuple, a SearchConfigException exception will be raised. """
        if not isinstance(value, tuple):
            raise SearchConfigException('Sort must be a tuple[str, str].')

        self._sort = value

    @property
    def start(self) -> int:
        """ Return the start. """
        return self._start

    @start.setter
    def start(self, value: int):
        """ Set the start. If the start is not an integer, a SearchConfigException exception will be raised. """
        if not isinstance(value, int):
            raise SearchConfigException('Start must be an integer.')

        self._start = value

    @property
    def limit(self) -> int:
        """ Return the limit. """
        return self._limit

    @limit.setter
    def limit(self, value: int):
        """ Set the limit. If the limit is not an integer, a SearchConfigException exception will be raised. """
        if not isinstance(value, int):
            raise SearchConfigException('Limit must be an integer.')

        self._limit = value

    @property
    def end(self) -> int:
        """ Return the end. """
        return self._start + self._limit

    @property
    def query(self) -> str | None:
        """ Return the query. """
        return self._query

    @query.setter
    def query(self, value: str | None):
        """ Set the query. If the query is not a string or is empty, a SearchConfigException exception will be
        raised. """
        if value is not None and (not isinstance(value, str) or not len(value.strip())):
            raise SearchConfigException('Query must be a string.')

        self._query = value

    @property
    def filters(self) -> dict[str, str] | None:
        """ Return the filters dict. """
        return self._filters

    @filters.setter
    def filters(self, value: dict[str, str] | None):
        """ Set the filters. If the filters are not a dict, a SearchConfigException exception will be raised. """
        if not isinstance(value, dict):
            raise SearchConfigException('Filters must be a dict[str, str].')

        self._filters = value

    @property
    def params(self) -> QueryDict | None:
        """ Return the params. """
        return self._request_query

    @params.setter
    def params(self, value: QueryDict | None):
        """ Set the params. If the params is not an QueryDict, a SearchConfigException exception will
        be raised. """
        if not isinstance(value, QueryDict):
            raise SearchConfigException('Request query must be an QueryDict.')

        self._request_query = value
        self._load_request_params()

    @property
    def var_start(self) -> str:
        """ Return the var_start. """
        return self._var_start

    @var_start.setter
    def var_start(self, value: str):
        """ Set the var_start. If the var_start is not a string, a SearchConfigException exception will be raised. """
        if not isinstance(value, str) or not len(value.strip()):
            raise SearchConfigException('Var_start must be a string.')

        self._var_start = value

    @property
    def var_limit(self) -> str:
        """ Return the var_limit. """
        return self._var_limit

    @var_limit.setter
    def var_limit(self, value: str):
        """ Set the var_limit. If the var_limit is not a string, a SearchConfigException exception will be raised. """
        if not isinstance(value, str) or not len(value.strip()):
            raise SearchConfigException('Var_limit must be a string.')

        self._var_limit = value

    @property
    def var_query(self) -> str:
        """ Return the var_query. """
        return self._var_query

    @var_query.setter
    def var_query(self, value: str):
        """ Set the var_query. If the var_query is not a string, a SearchConfigException exception will be raised. """
        if not isinstance(value, str) or not len(value.strip()):
            raise SearchConfigException('Var_query must be a string.')

        self._var_query = value

    """ SearchConfig Methods """

    def get_column(self, index_or_name: int | str) -> SearchColumn | None:
        """ Return a column by index or name. If the column does not exist, a SearchConfigException exception will be
        raised. """
        exception: SearchConfigException = SearchConfigException(f'The column "{index_or_name}" does not exist.')

        if isinstance(index_or_name, int) and index_or_name <= len(self._column_order):
            return self._columns[self._column_order[index_or_name].lstrip('-')]

        if isinstance(index_or_name, str) and isinstance(self._columns, dict) and index_or_name in self._columns:
            return self._columns[index_or_name]

        raise exception

    def get_column_names(self) -> list[str] | None:
        """ Return a list of column names. """
        if isinstance(self._columns, dict):
            return list(self._columns.keys())
        return None

    def has_column(self, name: str) -> bool:
        """ Return True if the column exists. """
        if not isinstance(self._columns, dict):
            return False

        return name in self._columns

    def has_columns(self) -> bool:
        """ Return True if the columns dict contains anything. """
        return isinstance(self._columns, dict) and len(self._columns)

    def add_column(self, name: str, column: SearchColumn | None = None) -> SearchColumn:
        """ Add a column by name. If the column already exists, a SearchConfigException exception will be raised. """
        self._init_columns()

        if not isinstance(column, SearchColumn):
            column = SearchColumn(name=name)

        if name in self._columns:
            raise SearchConfigException(f'Column already exists with name "{name}".')

        self._columns[name] = column

        return column

    def remove_column(self, name: str):
        """ Remove a column by name. If the column does not exist, a SearchConfigException exception will be raised. """
        if not isinstance(self._columns, dict) or name not in self._columns:
            raise SearchConfigException(f'The column "{name}" does not exist.')

        del self._columns[name]

    def set_column(self, name: str, column: SearchColumn | None = None):
        """ Set a column by name. If the column does not exist, it will be created. """
        self._init_columns()

        if not isinstance(column, SearchColumn):
            column = SearchColumn(name)

        self._columns[name] = column

    def _init_columns(self):
        """ Initialize the columns dict if it is not already set. """
        if not isinstance(self._columns, dict):
            self._columns = {}

    def _load_request_params(self):
        """ Load the request params. """
        if self._request_params_loaded or not self.has_columns():
            return

        if not isinstance(self._request_query, QueryDict):
            return

        if self._var_start in self._request_query:
            self.start = int(self._request_query[self._var_start])

        if self._var_limit in self._request_query:
            self.limit = int(self._request_query[self._var_limit])

        if self._var_query in self._request_query and len(value := self._request_query[self._var_query].strip()):
            self.query = value

        sortables: list = self.sortables

        for key, value in self._request_query.items():
            match = re.match(self._key_pattern, key)

            if match is None:
                continue

            column: SearchColumn | None = None
            config_type: str = match.group(1)
            index: int = int(match.group(2))
            key1: str = match.group(3)
            key2: str | None = None

            if len(match.groups()) > 3:
                key2 = match.group(4)

            if config_type == 'order':
                if not isinstance(self._sort_order, dict):
                    self._sort_order = {}

                if key1 == 'column':
                    column = self.get_column(sortables[int(value)])
                    dir_key: str = f'order[{index}][dir]'
                    if dir_key in self._request_query:
                        self._sort_order[index] = column, self._request_query[dir_key]
                    else:
                        self._sort_order[index] = column, SearchColumn.SORT_ASC

            if config_type == 'columns':
                if index >= len(sortables):
                    continue

                column = self.get_column(sortables[index])

                if key1 == 'searchable' and len(value := value.strip()):
                    column.searchable = value == 'true'

                if key1 == 'orderable' and len(value := value.strip()):
                    column.orderable = value == 'true'

                if key1 == 'search' and key2 == 'value' and len(value := value.strip()):
                    column.query = value

            if isinstance(column, SearchColumn):
                self.set_column(column.name, column)


class SearchApi:
    """ SearchApi Methods """

    @staticmethod
    def search(model: type[Model], config: SearchConfig) -> tuple[QuerySet, int, int]:
        query: Q | None = None

        # Obtain a model record set reference
        records: QuerySet = model.objects

        # Reduce the columns in the record set to those which are defined in the config.
        records = records.values(*config.get_column_names())

        # Cache a reference to the total number of records before filtering
        total_records: int = records.count()

        # Apply static column filters
        if isinstance(config.filters, dict):
            records = records.filter(**config.filters)

        # Apply text search
        for name, column in config.columns.items():
            op: str = 'contains' if column.case_sensitive else 'icontains'

            # Apply column specific text search filter
            if column.searchable and isinstance(column.query, str) and len(value := column.query.strip()):
                column_query: Q = Q(**{f'{name}__{op}': value})
                records = records.filter(column_query)

            # Update global text search filter to include the column if configured for global search
            if column.global_search and isinstance(config.query, str) and len(config.query.strip()):
                global_query: Q = Q(**{f'{name}__{op}': config.query})
                if query is None:
                    query = global_query
                else:
                    query |= global_query

        # Apply global text search filter
        if isinstance(query, Q):
            records = records.filter(query)

        # Apply sorting
        if isinstance(config.sort_order, dict):
            order: list[str] = []
            keys: list[int] = list(config.sort_order.keys())
            keys.sort()

            for key in keys:
                column, direction = config.sort_order[key]
                prepend: str = '-' if direction == SearchColumn.SORT_DESC else ''
                order.append(f'{prepend}{column.name}')

            records = records.order_by(*order)

        # Cache a reference to the total number of records before pagination
        total_display_records: int = records.count()

        # Apply paging
        records = records[config.start:config.end]

        return records, total_records, total_display_records

    @staticmethod
    def search_json(model: type[Model], config: SearchConfig) -> HttpResponse:
        search_results: tuple[QuerySet, int, int] = SearchApi.search(model, config)
        return SearchApi.get_response(search_results)

    @staticmethod
    def get_response_params(search_result: tuple[QuerySet, int, int]) -> dict[str, any]:
        records, total_records, total_display_records = search_result

        return {
            'data': list(records.values()) if isinstance(records, QuerySet) else [],
            'iTotalRecords': total_records,
            'iTotalDisplayRecords': total_display_records,
        }

    @staticmethod
    def get_response(search_result: tuple[QuerySet, int, int]) -> HttpResponse:
        import json
        from django.core.serializers.json import DjangoJSONEncoder
        params: dict[str, any] = SearchApi.get_response_params(search_result)
        return HttpResponse(json.dumps(params, cls=DjangoJSONEncoder), content_type='application/json')
