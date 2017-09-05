from bson.objectid import ObjectId


__obj_type_to_key_descriptor__ = {
    'Comment': 'object_id',
    'Event': 'id',
    'UserName': 'id',
    'Target': 'id',
    'Hash': 'id',
    'Dataset': 'id',
    'EmailAddress': 'id',
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
    from cripts.core.role import Role
    from cripts.events.event import Event
    from cripts.usernames.username import UserName
    from cripts.targets.target import Target
    from cripts.hashes.hash import Hash
    from cripts.datasets.dataset import Dataset
    from cripts.email_addresses.email_address import EmailAddress

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
    elif type_ == 'UserName':
        return UserName.objects(id=_id).first()
    elif type_ == 'Target':
        return Target.objects(id=_id).first()
    elif type_ == 'Hash':
        return Hash.objects(id=_id).first()
    elif type_ == 'Dataset':
        return Dataset.objects(id=_id).first()
    elif type_ == 'EmailAddress':
        return EmailAddress.objects(id=_id).first()
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
    from cripts.events.event import Event
    from cripts.usernames.username import UserName
    from cripts.targets.target import Target
    from cripts.hashes.hash import Hash
    from cripts.datasets.dataset import Dataset
    from cripts.email_addresses.email_address import EmailAddress

    # Make sure value is a string...
    value = str(value)

    # Use bson.ObjectId to make sure this is a valid ObjectId, otherwise
    # the queries below will raise a ValidationError exception.
    if (type_ in ['Comment','Event','UserName','Target','Hash','Dataset','EmailAddress'] and
       not ObjectId.is_valid(value.decode('utf8'))):
        return None
    
    if type_ == 'Comment':
        return Comment.objects(id=value).first()
    elif type_ == 'Event':
        return Event.objects(id=value).first()
    elif type_ == 'UserName':
        return UserName.objects(id=value).first()
    elif type_ == 'Target':
        return Target.objects(id=value).first()
    elif type_ == 'Hash':
        return Hash.objects(id=value).first()
    elif type_ == 'Dataset':
        return Dataset.objects(id=value).first()
    elif type_ == 'EmailAddress':
        return EmailAddress.objects(id=value).first()
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
    from cripts.events.event import Event
    from cripts.core.cripts_mongoengine import Action
    from cripts.core.source_access import SourceAccess
    from cripts.core.role import Role
    from cripts.usernames.username import UserName
    from cripts.targets.target import Target
    from cripts.hashes.hash import Hash
    from cripts.datasets.dataset import Dataset
    from cripts.email_addresses.email_address import EmailAddress

    if type_ == 'Comment':
        return Comment
    elif type_ == 'Action':
        return Action
    elif type_ == 'Event':
        return Event
    elif type_ == 'SourceAccess':
        return SourceAccess
    elif type_ == 'UserName':
        return UserName
    elif type_ == 'Target':
        return Target
    elif type_ == 'Hash':
        return Hash
    elif type_ == 'Dataset':
        return Dataset
    elif type_ == 'EmailAddress':
        return EmailAddress
    else:
        return None