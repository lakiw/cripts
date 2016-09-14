from bson.objectid import ObjectId


__obj_type_to_key_descriptor__ = {
    'Comment': 'object_id',
    'Event': 'id',
}

def class_from_id(type_, _id):
    """
    Return an instantiated class object.

    :param type_: The CRIPTs top-level object type.
    :type type_: str
    :param _id: The ObjectId to search for.
    :type _id: str
    :returns: class which inherits from
              :class:`cripts.core.cripts_mongoengine.CriptsBaseAttributes`
    """

    #Quick fail
    if not _id or not type_:
        return None

    # doing this to avoid circular imports
    from cripts.comments.comment import Comment
    from cripts.core.cripts_mongoengine import Action
    from cripts.core.source_access import SourceAccess
    from cripts.core.user_role import UserRole
    from cripts.events.event import Event

    # make sure it's a string
    _id = str(_id)

    # Use bson.ObjectId to make sure this is a valid ObjectId, otherwise
    # the queries below will raise a ValidationError exception.
    if not ObjectId.is_valid(_id.decode('utf8')):
        return None

    if type_ == 'Comment':
        return Comment.objects(id=_id).first()
    elif type_ == 'Event':
        return Event.objects(id=_id).first()
    elif type_ == 'Action':
        return Action.objects(id=_id).first()
    elif type_ == 'SourceAccess':
        return SourceAccess.objects(id=_id).first()
    elif type_ == 'UserRole':
        return UserRole.objects(id=_id).first()
    else:
        return None

def key_descriptor_from_obj_type(obj_type):
    return __obj_type_to_key_descriptor__.get(obj_type)

def class_from_value(type_, value):
    """
    Return an instantiated class object.

    :param type_: The CRIPTs top-level object type.
    :type type_: str
    :param value: The value to search for.
    :type value: str
    :returns: class which inherits from
              :class:`cripts.core.cripts_mongoengine.CriptsBaseAttributes`
    """

    #Quick fail
    if not type_ or not value:
        return None

    # doing this to avoid circular imports
    from cripts.comments.comment import Comment

    # Make sure value is a string...
    value = str(value)

    # Use bson.ObjectId to make sure this is a valid ObjectId, otherwise
    # the queries below will raise a ValidationError exception.
    if (type_ in ['Comment',] and
       not ObjectId.is_valid(value.decode('utf8'))):
        return None

    if type_ == 'Comment':
        return Comment.objects(id=value).first()
    else:
        return None

def class_from_type(type_):
    """
    Return a class object.

    :param type_: The CRIPTs top-level object type.
    :type type_: str
    :returns: class which inherits from
              :class:`cripts.core.cripts_mongoengine.CriptsBaseAttributes`
    """

    #Quick fail
    if not type_:
        return None

    # doing this to avoid circular imports
    from cripts.comments.comment import Comment
    from cripts.core.cripts_mongoengine import Action
    from cripts.core.source_access import SourceAccess
    from cripts.core.user_role import UserRole

    if type_ == 'Comment':
        return Comment
    elif type_ == 'UserRole':
        return UserRole
    else:
        return None
