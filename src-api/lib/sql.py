from typing import Any

from sqlalchemy import Select

from models.api import ListParamsModel
from models.enums import QueryLogicOperatorEnum


OPERATOR_MAP = {
    QueryLogicOperatorEnum.EQUALS: lambda field, value: field == value,
    QueryLogicOperatorEnum.NOT_EQUALS: lambda field, value: field != value,
    QueryLogicOperatorEnum.GT: lambda field, value: field > value,
    QueryLogicOperatorEnum.LT: lambda field, value: field < value,
    QueryLogicOperatorEnum.GTE: lambda field, value: field >= value,
    QueryLogicOperatorEnum.LTE: lambda field, value: field <= value,
    QueryLogicOperatorEnum.IS: lambda field, value: field.is_(value),
    QueryLogicOperatorEnum.IS_NOT: lambda field, value: field.isnot(value),
    QueryLogicOperatorEnum.CONTAINS: lambda field, value: field.like(f"%{value}%"),
    QueryLogicOperatorEnum.NOT_CONTAINS: lambda field, value: ~field.like(f"%{value}%"),
    QueryLogicOperatorEnum.STARTS_WITH: lambda field, value: field.like(f"{value}%"),
    QueryLogicOperatorEnum.ENDS_WITH: lambda field, value: field.like(f"%{value}"),
    QueryLogicOperatorEnum.BEFORE: lambda field, value: field < value,
    QueryLogicOperatorEnum.AFTER: lambda field, value: field > value,
    QueryLogicOperatorEnum.ON_OR_BEFORE: lambda field, value: field <= value,
    QueryLogicOperatorEnum.ON_OR_AFTER: lambda field, value: field >= value,
    QueryLogicOperatorEnum.IS_EMPTY: lambda field, value: field.is_(value),
    QueryLogicOperatorEnum.IS_NOT_EMPTY: lambda field, value: field.isnot(value),
    QueryLogicOperatorEnum.IS_ANY_OF: lambda field, value_list: field.in_(value_list),
}


class SqlQueryBuilder:
    """
    Provides an interface for building SQLAlchemy ORM queries with optional manipulation for filtering, sorting,
    and paging.
    """

    @staticmethod
    def apply_params(params: ListParamsModel, stmt: Select[Any], model: type):
        """Applies the given params model to the given query statement and returns the modified statement."""
        from uuid import UUID
        from loguru import logger
        from sqlalchemy import and_, or_, cast, String
        from models.enums import FilterLogicOperatorEnum

        # Apply filtering
        if params.filters.items:
            conjunction = and_ if params.filters.logic_operator == FilterLogicOperatorEnum.AND else or_
            clauses = []

            for item in params.filters.items:
                try:
                    # XXX: This approach might expose a bit of a security hole without forcing a fixed field mapping
                    field_attribute = getattr(model, item.field)
                    field_type = field_attribute.property.columns[0].type.python_type
                    operator_func = OPERATOR_MAP.get(item.operator)

                    if field_type is UUID:
                        field_attribute = cast(field_attribute, String)

                    if field_attribute is not None and operator_func is not None:
                        clause = operator_func(field_attribute, item.value)
                        clauses.append(clause)

                except ValueError:
                    logger.error(f'SqlQueryBuilder.apply_params(): Failed to apply field filter: field: {item.field},  value: {item.value}')

            if clauses:
                stmt = stmt.filter(conjunction(*clauses))

        # Apply sorting
        if params.sorts:
            for sort in params.sorts:
                stmt = stmt.order_by(getattr(getattr(model, sort.field), sort.direction)())

        # Apply pagination
        stmt = stmt.limit(params.pagination.page_size).offset(params.pagination.offset)

        return stmt
