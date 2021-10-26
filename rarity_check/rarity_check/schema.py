import graphene
from graphene_django import DjangoObjectType

from project.models import Project, TraitType, TraitValue, Token, TokenType

class TokenTypeType(DjangoObjectType):
    class Meta:
        model = TokenType
        fields = ("name",)

class TokenType(DjangoObjectType):
    class Meta:
        model = Token
        fields = ("token_type", "number", "image_url",
                "rank", "score", "traits")

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
    all_proj_tokens = graphene.List(TokenType,
            proj_name=graphene.String(required=True))
    token_by_number = graphene.Field(TokenType,
            number=graphene.Int(required=True))
    tokens_by_ranks = graphene.List(TokenType,
            proj_name=graphene.String(required=True),
            start_rank=graphene.Int(required=True),
            end_rank=graphene.Int(required=True))

    def resolve_all_tokens(root, info):
        return Token.objects.all()

    def resolve_all_proj_tokens(root, info, proj_name):
        try:
            proj_obj = Project.objects.get(name=proj_name)
            return Token.objects.filter(project=proj_obj)
        except Project.DoesNotExist:
            return None

    def resolve_token_by_number(root, info, number):
        try:
            return Token.objects.get(number=number)
        except Token.DoesNotExist:
            return None

    def resolve_tokens_by_ranks(root, info, proj_name,
            start_rank, end_rank):
        try:
            proj_obj = Project.objects.get(name=proj_name)
            return Token.objects.filter(
                    project=proj_obj)[start_rank - 1:end_rank]
        except Project.DoesNotExist:
            return None

schema = graphene.Schema(query=Query)
