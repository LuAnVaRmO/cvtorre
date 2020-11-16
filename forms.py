#!/usr/bin/python3
from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField


class CreationForm(Form):
    username = StringField('Torre\'s Username',
                           [
                               validators.Required(message="Username Required"),
                           ]
                           )
    document = StringField('Document/ID')
    address = StringField('Address')
    birth = StringField('Birth')
    nation = StringField('Nationality')
    phone = StringField('Phone')
    email = EmailField('Email')


class OportunityForm(Form):
    oportunity = StringField('oportunity',
                             [
                                 validators.Required(message="This field must not be empty"),
                             ]
                             )
    offset = StringField('Offset')
    size = StringField('Size of oportunities')
    aggregate = StringField('Aggregate')

