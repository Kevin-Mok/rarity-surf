import graphene
from graphene_django import DjangoObjectType

from project.models import Project, TraitType, TraitValue, Token

class TokenType(DjangoObjectType):
    class Meta:
        model = Token
        fields = ("number", "image_url", "score", "traits")

class TraitValueType(DjangoObjectType):
    class Meta:
        model = TraitValue
        fields = ("trait_type", "name", "rarity", "score")

class TraitTypeType(DjangoObjectType):
    class Meta:
        model = TraitType
        fields = ("name",)

class Query(graphene.ObjectType):
    all_tokens = graphene.List(TokenType)
    token_by_number = graphene.Field(TokenType,
            number=graphene.Int(required=True))

    def resolve_all_tokens(root, info):
        # We can easily optimize query count in the resolve method
        return Token.objects.all()

    def resolve_token_by_number(root, info, number):
        try:
            return Token.objects.get(number=number)
        except Token.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)
