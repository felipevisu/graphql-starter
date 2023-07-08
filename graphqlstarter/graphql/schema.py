import graphene

from .blog.schema import Mutation as BlogMutation
from .blog.schema import Query as BlogQuery


class Query(BlogQuery):
    pass


class Mutation(BlogMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
