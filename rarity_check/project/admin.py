from django.contrib import admin

from .models import Project, TraitType, TraitValue, Token

admin.site.register(Project)
admin.site.register(TraitType)
admin.site.register(TraitValue)
admin.site.register(Token)
