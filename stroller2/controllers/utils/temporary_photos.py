import logging
from PIL import Image
from tgext.datahelpers.utils import fail_with
from tg import TGController, expose, validate, session
from stroller2.model import TemporaryPhotosBucket, BucketProductImage
from datetime import datetime
from tw2.forms import FileValidator
from tw2.core import IntValidator
from bson import ObjectId

log = logging.getLogger('tavolaclandestina')


class TemporaryPhotosUploader(TGController):
    @classmethod
    def get_bucket(cls):
        bucket = None
        bucket_id = session.get('temporary_photos_bucket_id')
        if bucket_id is not None:
            bucket = TemporaryPhotosBucket.query.get(
                _id=ObjectId(bucket_id)
            )

        if bucket is None:
            bucket = TemporaryPhotosBucket(
                created_at=datetime.utcnow()
            )

        session['temporary_photos_bucket_id'] = str(bucket._id)
        session.save()
        return bucket

    @classmethod
    def new_bucket(cls):
        bucket = TemporaryPhotosBucket(created_at=datetime.utcnow())
        session['temporary_photos_bucket_id'] = str(bucket._id)
        session.save()
        return bucket

    @classmethod
    def current_photos(cls):
        bucket = cls.get_bucket()
        return [
            dict(
                url=value[0],
                uid=str(idx),
                full_url=value[1]
            )
            for idx, value in enumerate(BucketProductImage.query.find(
                {'_id': {'$in': bucket.photos}},
                {'image.thumb_url': 1, 'image.url': 1}
            ))]

    @classmethod
    def recover_photos(cls, photos):
        bucket = cls.get_bucket()
        bucket.photos = photos
        return [
            dict(
                url=p.image.thumb_url,
                uid=str(idx),
                full_url=p.image.url
            ) for idx, p in enumerate(bucket.images)
        ]

    @classmethod
    def save_image(cls, file, idx=None):
        bucket = cls.get_bucket()
        image = BucketProductImage(
            bucket_id=bucket._id,
            image=file
        )
        if not idx:
            TemporaryPhotosBucket.query.update(
                {'_id': bucket._id},
                {'$push': {'photos': image._id}}
            )
        else:
            TemporaryPhotosBucket.query.update(
                {'_id': bucket._id},
                {'$set': {f'photos.{idx}': image._id}}
            )
    # @classmethod
    # def save_image(cls, file):
    #     attached_image = AttachedImage(file.file, file.filename)
    #     attached_image.thumbnail_size = (200, 200)
    #     attached_image.write()
    #     image_data = {'file': attached_image.local_path,
    #                   'url': attached_image.url,
    #                   'filename': attached_image.filename,
    #                   'uuid': attached_image.uuid,
    #                   'thumb_local_path': attached_image.thumb_local_path,
    #                   'thumb_url': attached_image.thumb_url}
    #     return image_data

    @expose('json')
    @validate({
            'file': FileValidator(required=True),
            'uid': IntValidator()
        },
        error_handler=fail_with(403)
    )
    def save(self, file, uid=None):
        try:
            Image.open(file.file)
            file.file.seek(0)
        except:
            log.exception('Failed to upload image')
            return dict(photos=self.current_photos())

        if uid is None:
            self.save_image(file)
        else:
            self.save_image(file, uid)

        return dict(photos=self.current_photos())

    @expose('json')
    @validate({'uid': IntValidator(required=True)},
              error_handler=fail_with(403))
    def remove(self, uid=None):
        bucket = self.get_bucket()
        try:
            bucket.photos.pop(uid)
        except:
            log.exception('Trying to pop an unexisting image')

        return dict(photos=self.current_photos())


