from datetime import datetime
from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass
from stroller2.model import DBSession
from tgext.pluggable import app_model


class TemporaryPhotosBucket(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'temporary_photos_bucket'
        unique_indexes = [('created_at',),]

    _id = FieldProperty(s.ObjectId)
    created_at = FieldProperty(s.DateTime, required=True, if_missing=datetime.utcnow)
    photos = FieldProperty([{'file': s.String(required=True),
                             'url': s.String(required=True),
                             'thumb_url': s.String(required=True),
                             'thumb_local_path': s.String(required=True),
                             'uuid': s.String(required=True),
                             'filename': s.String(required=True)}])

class UserAddress(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'user_addresses'
        indexes = [('user_id',),]

    _id = FieldProperty(s.ObjectId)
    user = RelationProperty(app_model.User)
    user_id = ForeignIdProperty(app_model.User)
    shipping_address = FieldProperty({
        'receiver': s.String,
        'address': s.String,
        'city': s.String,
        'province': s.String,
        'state': s.String,
        'country': s.String,
        'zip': s.String,
        'details': s.Anything
    })
