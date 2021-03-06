from base.properties import node_public_properties, link_public_properties
from flask_wtf import FlaskForm
from objects.models import link_class, node_class
from wtforms import (
    BooleanField,
    FloatField,
    PasswordField,
    SelectField,
    TextField
)
from wtforms.validators import optional

## Object creation


class AddObjectForm(FlaskForm):
    name = TextField('Name')
    description = TextField('Description')
    location = TextField('Location')
    vendor = TextField('Vendor')

# nodes can be added to the database either one by one via the AddNode
# form, or all at once by importing an Excel or a CSV file.


class AddNode(AddObjectForm):
    node_type = [(t, t) for t in node_class]
    type = SelectField('Type', choices=node_type)
    ip_address = TextField('IP address', [optional()])
    operating_system = TextField('Operating System', [optional()])
    os_version = TextField('OS version', [optional()])
    longitude = FloatField('Longitude', default=0.)
    latitude = FloatField('Latitude', default=0.)
    secret_password = PasswordField('Secret password')


class AddLink(AddObjectForm):
    link_type = [(t, t) for t in link_class]
    type = SelectField('Type', choices=link_type)
    source = SelectField('Source', choices=())
    destination = SelectField('Destination', choices=())

## Object filtering


def configure_form(cls):
    cls.node_properties = node_public_properties
    cls.link_properties = link_public_properties
    for property in node_public_properties:
        setattr(cls, 'node_' + property, TextField(property))
        setattr(cls, 'node_' + property + '_regex', BooleanField('Regex'))
    for property in link_public_properties:
        setattr(cls, 'link_' + property, TextField(property))
        setattr(cls, 'link_' + property + '_regex', BooleanField('Regex'))
    return cls


@configure_form
class FilteringForm(FlaskForm):
    filters = SelectField('Filters', choices=())
    name = TextField('Name')
