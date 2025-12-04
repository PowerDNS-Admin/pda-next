from typing import Any, Optional

from pydantic import ConfigDict, Field

from models import BaseModel
from models.enums import SortDirectionEnum, FilterLogicOperatorEnum, QueryLogicOperatorEnum


class BaseApiModel(BaseModel):
    """Provides an abstract API schema class."""
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SortModel(BaseApiModel):
    """Provides an abstract API schema class for sorting parameters of record listing routes."""

    field: str = Field(
        title='Sort Field Name',
        description='Field name to be sorted.',
    )
    """Field name to be sorted."""

    direction: SortDirectionEnum = Field(
        title='Sort Direction',
        description='Direction to sort field in.',
        default=SortDirectionEnum.ASC,
        alias='sort',
        examples=[SortDirectionEnum.ASC, SortDirectionEnum.DESC],
    )
    """Direction to sort field in."""


class FilterItem(BaseApiModel):
    """Represents a FilterModel filtering item."""

    id: Optional[int] = Field(
        title='Filter ID',
        description='The unique identifier of the filter.',
        default=None,
    )
    """The unique identifier of the filter."""

    field: str = Field(
        title='Filter Field Name',
        description='Field name to be filtered.',
    )
    """Field name to be filtered."""

    value: Optional[Any] = Field(
        title='Filter Value',
        description='Value to be filtered on.',
        default=None,
    )
    """Value to be filtered on."""

    operator: QueryLogicOperatorEnum = Field(
        title='Filter Operator',
        description='Filter operator to be applied.',
        default=QueryLogicOperatorEnum.EQUALS,
        examples=[
            QueryLogicOperatorEnum.EQUALS, QueryLogicOperatorEnum.NOT_EQUALS,
            QueryLogicOperatorEnum.IS, QueryLogicOperatorEnum.IS_NOT,
            QueryLogicOperatorEnum.LT, QueryLogicOperatorEnum.LTE,
            QueryLogicOperatorEnum.GT, QueryLogicOperatorEnum.GTE,
        ],
    )
    """Filter operator to be applied."""


class FilterModel(BaseApiModel):
    """Provides an abstract API schema class for filtering parameters of record listing routes."""

    items: list[FilterItem] = Field(
        title='Filter Items',
        description='A list of items to apply filtering on.',
        default_factory=list,
    )
    """A list of items to apply filtering on."""

    logic_operator: FilterLogicOperatorEnum = Field(
        title='Logic Operator',
        description='The logic operator to apply filtering with.',
        alias='logicOperator',
        examples=[FilterLogicOperatorEnum.AND, FilterLogicOperatorEnum.OR],
    )
    """The logic operator to apply filtering with."""

    quick_filter_logic_operator: FilterLogicOperatorEnum = Field(
        title='Quick Filter Logic Operator',
        description='The logic operator to apply quick filtering with.',
        alias='quickFilterLogicOperator',
        examples=[FilterLogicOperatorEnum.AND, FilterLogicOperatorEnum.OR],
    )
    """The logic operator to apply quick filtering with."""

    quick_filter_values: list = Field(
        title='Quick Filter Values',
        description='A list of values to apply quick filtering with.',
        alias='quickFilterValues',
    )
    """A list of values to apply quick filtering with."""


class PaginationModel(BaseApiModel):
    """Provides an abstract API schema class for pagination parameters of record listing routes."""

    page: int = Field(
        title='Page Index',
        description='The page index of the record set to retrieve.',
        default=0,
    )
    """The page index of the record set to retrieve."""

    page_size: int = Field(
        title='Page Size',
        description='The number of records to retrieve per page.',
        default=100,
        alias='pageSize',
    )
    """The number of records to retrieve per page."""

    @property
    def offset(self) -> int:
        """The offset index for the associated query."""
        return ((self.page if self.page > 0 else 1) - 1) * self.page_size


class ListParamsModel(BaseApiModel):
    """Provides an abstract API schema class for handling manipulation parameters of record listing routes."""

    sorts: Optional[list[SortModel]] = Field(
        title='Sorting Model',
        description='Provides the record sorting model for the request.',
        default_factory=list[SortModel],
        alias='sortModel',
    )
    """Provides the record sorting model for the request."""

    filters: FilterModel = Field(
        title='Filter Model',
        description='Provides the record filtering model for the request.',
        default_factory=FilterModel,
        alias='filterModel',
    )
    """Provides the record filtering model for the request."""

    pagination: PaginationModel = Field(
        title='Pagination Model',
        description='Provides the record pagination model for the request.',
        default_factory=PaginationModel,
        alias='paginationModel',
    )
    """Provides the record pagination model for the request."""

    group_keys: Optional[list[str]] = Field(
        title='Group Keys',
        description='Provides a list of record grouping keys.',
        default=None,
        alias='groupKeys',
    )
    """Provides a list of record grouping keys."""

    start: Optional[int] = Field(
        title='Start Index',
        description='Provides the start index for the records to be returned.',
        default=None,
    )
    """Provides the start index for the records to be returned."""

    end: Optional[int] = Field(
        title='End Index',
        description='Provides the end index for the records to be returned.',
        default=None,
    )
    """Provides the end index for the records to be returned."""


from .auth import *
