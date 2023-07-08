import graphene

from ...blog import models
from ..core.mutations import ModelDeleteMutation, ModelMutation
from .types import Category


class CategoryInput(graphene.InputObjectType):
    name = graphene.String()


class CategoryCreate(ModelMutation):
    category = graphene.Field(Category)

    class Arguments:
        input = CategoryInput(required=True)

    class Meta:
        model = models.Category
        object_type = Category


class CategoryDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID()

    class Meta:
        model = models.Category
        object_type = Category
