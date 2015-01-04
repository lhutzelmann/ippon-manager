import collections
from wheezy.validation import Validator
from wheezy.validation.rules import length
from wheezy.validation.rules import required

from ipponmanager.tournament.datamodel import Tournament
_ = lambda s: s     # i18n


class ValidatorRegistry(object):
    """ Registry which maps data models to validators.
    Validators must provide a method "validate" with two arguments: data_object
    and an errors dictionary for an validation errors found.

    Needs not be instantiated, as data is managed on class level.
    """

    validators = {}

    @classmethod
    def register(cls, class_type, validator):
        """
        Register a validator for the given data model class.
        :param class_type: data model class
        :param validator: validator object
        :return:
        """
        type_validators = cls.validators.setdefault(class_type, [])
        if validator not in type_validators:
            type_validators.append(validator)

    @classmethod
    def unregister(cls, class_type, validator):
        """
        Remove registration of a validator for a given data model class.
        :param class_type: data model class
        :param validator: validator object
        :return:
        """
        type_validators = cls.validators.get(class_type, [])
        if validator in type_validators:
            type_validators.remove(validator)

    @classmethod
    def validate(cls, data_object, errors):
        """
        Perform the validations for the given data object.
        :param data_object: The data model instance
        :param errors: a dictionary which will contain validation errors
        :return: True if the validation succeeded
        """
        class_type = data_object.__class__
        return cls.validate_values(class_type, data_object, errors)

    @classmethod
    def validate_values(cls, class_type, data, errors):
        """
        Perform the validations for the given data object on the given values.
        :param class_type: data model class
        :param data: a data object or a dictionary containing key/value pairs
        :param errors: a dictionary which will contain validation errors
        :return: True if the validation succeeded
        """
        type_validators = cls.validators.get(class_type, [])
        is_valid = True
        for validator in type_validators:
            is_valid = validator.validate(data, errors) and is_valid
        return is_valid


class AutoLengthRule(object):
    """ Wheezy validation rule to validate maximum length of string based
        on SQLAlchemy Column information.
    """
    __slots__ = ('data_model_class', 'message_template')

    def __init__(self, data_model_class, message_template=None):
        self.data_model_class = data_model_class
        self.message_template = message_template or _(
            "Field's size exceeds its maximum value.")

    def __call__(self, message_template):
        """ Let you customize message template.
        """
        return AutoLengthRule(message_template)

    def validate(self, value, name, model, result, gettext):
        max_len = self.data_model_class.max_str_len(name)
        if max_len is not None and len(value) > max_len:
            result.append(gettext(self.message_template))
            return False
        return True

auto_length = AutoLengthRule

tournament_validator = Validator({
    'title': [required, auto_length(Tournament)],
    'description': [required, length(min=5), auto_length(Tournament)],
    'organiser': [required, length(min=5), auto_length(Tournament)],
})
