"""
This is the people module and supports all the ReST actions for the
PEOPLE collection
"""

from flask import make_response, abort
from config import db
from models import Person, PersonSchema


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    people = Person.query.order_by(Person.lname).all()
    person_schema = PersonSchema(many=True)
    data = person_schema.dump(people)
    return data

def read_one(person_id):
    """
    This function responds to a request for /api/people/{lname}
    with one matching person from people
    :param lname:   last name of person to find
    :return:        person matching last name
    """
    person = Person.query.filter(Person.person_id==person_id).one_or_none()

    if person is not None:
        person_schema = PersonSchema()
        return person_schema.dump(person)
    else:
        abort(404, f"Person not found for Id: {person_id}.")

def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    lname = person.get("lname")
    fname = person.get("fname")

    existing_person = Person.query \
        .filter(Person.fname == fname) \
        .filter(Person.lname == lname) \
        .one_or_none()

    if existing_person is None:
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session)

        db.session.add(Person(fname=fname, lname=lname))
        # db.session.add(new_person)
        db.session.commit()

        data = schema.dump(new_person)
        return data, 201
    
    else:
        abort(409, f"Person {fname} {lname} already exists.")

def update(person_id, person):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    update_person = Person.query.filter(
        Person.person_id == person_id
    ).one_or_none()

    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )

    if update_person is None:
        abort(
            404,
            f"Person not found for Id: {person_id}."
        )
    
    elif existing_person is not None and existing_person.person_id != person_id:
        abort(
            409,
            f"Person {fname} {lname} already exists."
        )

    else:
        update = Person(fname=fname, lname=lname)
        update.person_id = person_id
        schema = PersonSchema()
        # update = schema.load(person, session=db.session)
        # update.person_id = update_person.person_id
        db.session.merge(update)
        db.session.commit()
        update_person = schema.load(person, session=db.session)
        data = schema.dump(update_person)
        return data, 200

def delete(person_id):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(
            f"Person {person_id} ({person.fname} {person.lname}) deleted.", 200
        )

    else:
        abort(404, f"Person not found for Id: {person_id}.")
