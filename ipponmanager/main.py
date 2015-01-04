import sys

from wheezy.core.comp import u

from ipponmanager.dataaccess import DalSqlAlchemy
from ipponmanager.tournament.validation import ValidatorRegistry
from ipponmanager.tournament.validation import tournament_validator
from ipponmanager.tournament.datamodel import Tournament


def dump_validation_errors(errors):
    """
    Prints the validation_errors.
    :param errors: dictionary, key = field name, value = list of error messages
    :return:
    """
    for field, errorlist in errors.items():
        for error in errorlist:
            print("ERROR IN FIELD: {} - {}".format(field, error))

if __name__ == '__main__':
    # Test code
    ValidatorRegistry.register(Tournament, tournament_validator)

    dal = DalSqlAlchemy()
    dal.create_database()
    session = dal.get_session()

    # Example 1: Validate before creating data object
    tournament_dict = dict(
        title=u('Vereinsmeisterschaften'),
        organiser=u('JC Ettlingen'),
        description=u('Vereinsmeisterschaften des JC Ettlingen'))

    errors = {}
    if not ValidatorRegistry.validate_values(Tournament, tournament_dict,
                                             errors):
        dump_validation_errors(errors)
        session.abort()
        sys.exit(1)

    t = dal.new(Tournament, **tournament_dict)
    session.commit()
    print(t.id)

    # Example 2: Validate after creating data object
    t2 = dal.new(Tournament, title="TITLE", organiser="ORGANISER",
                 description="DESCRIPTION")
    if not ValidatorRegistry.validate(t2, errors):
        dump_validation_errors(errors)
        session.abort()
        sys.exit(1)
    session.commit()
    print(t2.id)
