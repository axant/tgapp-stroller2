from datetime import datetime

from depot.fields.interfaces import FileFilter
from depot.manager import DepotManager
from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass
from stroller2.model import DBSession
from tgext.pluggable import app_model
from depot.fields.ming import UploadedFileProperty
from depot.fields.specialized.image import UploadedImageWithThumb as UploadedThumb


class UploadedImageWithThumb(UploadedThumb):
    thumbnail_size = (200, 200)


class BucketProductImage(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'bucket_product_image'
        indexes = [('bucket_id', )]

    _id = FieldProperty(s.ObjectId)

    image = UploadedFileProperty(
            upload_storage='product_images',
            upload_type=UploadedImageWithThumb
        )

    bucket_id = ForeignIdProperty('TemporaryPhotosBucket')
    bucket = RelationProperty('TemporaryPhotosBucket')


class TemporaryPhotosBucket(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'temporary_photos_bucket'
        unique_indexes = [('created_at',), ]

    _id = FieldProperty(s.ObjectId)
    created_at = FieldProperty(s.DateTime, required=True, if_missing=datetime.utcnow)
    photos = ForeignIdProperty(BucketProductImage, uselist=True)


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
