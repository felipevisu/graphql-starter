import graphene

from ..core.connection import create_connection_slice, filter_connection_queryset
from ..core.fields import FilterConnectionField
from .filters import CategoryFilterInput
from .mutations import CategoryCreate, CategoryDelete
from .resolvers import resolve_categories, resolve_category_by_name
from .sorters import CategorySortingInput
from .types import Category, CategoryCountableConnection


class Query(graphene.ObjectType):
    categories = FilterConnectionField(
        CategoryCountableConnection,
        filter=CategoryFilterInput(),
        sort_by=CategorySortingInput(),
    )
    category = graphene.Field(
        Category,
        id=graphene.Argument(graphene.ID),
        name=graphene.Argument(graphene.String),
    )

    @staticmethod
    def resolve_category(_root, _info, *, id=None, name=None):
        if id:
            return None
        if name:
            return resolve_category_by_name(name=name)

    @staticmethod
    def resolve_categories(_root, info, **kwargs):
        qs = resolve_categories()
        qs = filter_connection_queryset(qs, kwargs)
        return create_connection_slice(qs, info, kwargs, CategoryCountableConnection)


class Mutation(graphene.ObjectType):
    category_create = CategoryCreate.Field()
    category_delete = CategoryDelete.Field()
