import itertools

import graphene
from django.db import models
from django_filters.filterset import FILTER_FOR_DBFIELD_DEFAULTS, BaseFilterSet
from graphene import Argument, InputField, InputObjectType, String
from graphene.types.inputobjecttype import InputObjectTypeOptions
from graphene.types.utils import yank_fields_from_attrs

from ..filters import GlobalIDFilter, GlobalIDMultipleChoiceFilter
from .common import NonNullList
from .converter import convert_form_field

GLOBAL_ID_FILTERS = {
    models.AutoField: {"filter_class": GlobalIDFilter},
    models.OneToOneField: {"filter_class": GlobalIDFilter},
    models.ForeignKey: {"filter_class": GlobalIDFilter},
    models.ManyToManyField: {"filter_class": GlobalIDMultipleChoiceFilter},
    models.ManyToOneRel: {"filter_class": GlobalIDMultipleChoiceFilter},
    models.ManyToManyRel: {"filter_class": GlobalIDMultipleChoiceFilter},
}


class GraphQLFilterSetMixin(BaseFilterSet):
    FILTER_DEFAULTS = dict(
        itertools.chain(FILTER_FOR_DBFIELD_DEFAULTS.items(), GLOBAL_ID_FILTERS.items())
    )


def get_filterset_class(filterset_class=None):
    return type(
        "GraphQL{}".format(filterset_class.__name__),
        (filterset_class, GraphQLFilterSetMixin),
        {},
    )


class FilterInputObjectType(InputObjectType):
    @classmethod
    def __init_subclass_with_meta__(
        cls, _meta=None, model=None, filterset_class=None, fields=None, **options
    ):
        cls.custom_filterset_class = filterset_class
        cls.filterset_class = None
        cls.fields = fields
        cls.model = model

        if not _meta:
            _meta = InputObjectTypeOptions(cls)

        fields = cls.get_filtering_args_from_filterset()
        fields = yank_fields_from_attrs(fields, _as=InputField)
        if _meta.fields:
            _meta.fields.update(fields)
        else:
            _meta.fields = fields

        super().__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def get_filtering_args_from_filterset(cls):
        if not cls.custom_filterset_class:
            raise ValueError("Provide filterset class")

        cls.filterset_class = get_filterset_class(cls.custom_filterset_class)

        args = {}
        for name, filter_field in cls.filterset_class.base_filters.items():
            input_class = getattr(filter_field, "input_class", None)
            if input_class:
                field_type = convert_form_field(filter_field)
            else:
                field_type = convert_form_field(filter_field.field)
                field_type.description = getattr(filter_field, "help_text", "")
            kwargs = getattr(field_type, "kwargs", {})
            field_type.kwargs = kwargs
            args[name] = field_type
        return args


class ChannelFilterInputObjectType(FilterInputObjectType):
    channel = Argument(String)

    class Meta:
        abstract = True


class StringFilterInput(graphene.InputObjectType):
    eq = graphene.String(required=False)
    one_of = NonNullList(graphene.String, required=False)


class WhereInputObjectType(FilterInputObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, _meta=None, **options):
        super().__init_subclass_with_meta__(_meta=_meta, **options)
        cls._meta.fields.update(
            {
                "AND": graphene.Field(
                    NonNullList(
                        cls,
                    )
                ),
                "OR": graphene.Field(
                    NonNullList(
                        cls,
                    )
                ),
            }
        )
