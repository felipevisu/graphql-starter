from functools import singledispatch

import graphene
from django import forms
from django.core.exceptions import ImproperlyConfigured

from ..filters import (
    EnumFilter,
    GlobalIDFormField,
    GlobalIDMultipleChoiceField,
    ListObjectTypeFilter,
    ObjectTypeFilter,
)
from .common import NonNullList


def get_form_field_description(field):
    return str(field.help_text) if field.help_text else None


@singledispatch
def convert_form_field(field):
    raise ImproperlyConfigured(
        "Don't know how to convert the Django form field %s (%s) "
        "to Graphene type" % (field, field.__class__)
    )


@convert_form_field.register(forms.CharField)
def convert_form_field_to_string(field):
    return graphene.String(
        description=get_form_field_description(field), required=field.required
    )


@convert_form_field.register(forms.NullBooleanField)
def convert_form_field_to_nullboolean(field):
    return graphene.Boolean(description=get_form_field_description(field))


@convert_form_field.register(forms.DecimalField)
@convert_form_field.register(forms.FloatField)
def convert_form_field_to_float(field):
    return graphene.Float(description=field.help_text, required=field.required)


@convert_form_field.register(ObjectTypeFilter)
@convert_form_field.register(EnumFilter)
def convert_convert_enum(field):
    return field.input_class()


@convert_form_field.register(GlobalIDFormField)
def convert_form_field_to_id(field):
    return graphene.ID(required=field.required)


@convert_form_field.register(ListObjectTypeFilter)
def convert_list_object_type(field):
    return NonNullList(field.input_class)


@convert_form_field.register(GlobalIDMultipleChoiceField)
def convert_form_field_to_list(field):
    return NonNullList(graphene.ID, required=field.required)
