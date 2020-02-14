import logging
from PIL import Image
from tgext.datahelpers.utils import fail_with
from tgext.pluggable import app_model
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
        photos = []
        for idx, p_id in enumerate(bucket.photos):
            p = BucketProductImage.query.get(_id=p_id)
            photos.append(dict(
                url=p.image.thumb_url,
                uid=str(idx),
                full_url=p.image.url
            ))

        # photos  = [
        #     dict(
        #         url=value.image.thumb_url,
        #         uid=str(idx),
        #         full_url=value.image.url,
        #     ) 
        #     for idx, value in enumerate(BucketProductImage.query.find(
        #         {'_id': {'$in': bucket.photos}},
        #         {'image.thumb_url': 1, 'image.url': 1}
        #     )) if value.image is not None
        # ]
        # for image in BucketProductImage.query.find({'_id': {'$in': bucket.photos}}, {'image.thumb_url': 1, 'image.url': 1}):
        #     print(f'got image: {image.image}')
        # for p in bucket.photos_rel:
        #     if p.image is None:
        #         print('even here is None')
        # tried also
        # [print(img) for img in mapper(BucketProductImage).collection.m.collection.find({'_id': {'$in': bucket.photos}}, {'image.thumb_url': 1, 'image.url': 1})]
        # app_model.DBSession.impl.find(mapper(BucketProductImage).collection, {'_id': {'$in': bucket.photos}}, {'image.thumb_url': 1, 'image.url': 1}).all()
        # this should not be used, and doesn't work either
        # BucketProductImage.query.find({'bucket_id': bucket._id}).all()
        return photos

    @classmethod
    def recover_photos(cls, photos):
        bucket = cls.get_bucket()
        bucket.photos = photos
        recovered = [
            # BROKEN: p.image is None with find, but with get it is full of informations...
            # dict(
            #     url=p.image.thumb_url,
            #     uid=str(idx),
            #     full_url=p.image.url
            # ) for idx, p in enumerate(BucketProductImage.query.find(
            #     {'_id': {'$in': photos}},
            #     {'image.thumb_url': 1, 'image.url': 1}
            # )) if p.image is not None
        ]
        for idx, p_id in enumerate(photos):
            p = BucketProductImage.query.get(_id=p_id)
            recovered.append(dict(
                url=p.image.thumb_url,
                uid=str(idx),
                full_url=p.image.url
            ))
        return recovered

    @classmethod
    def save_image(cls, file, idx=None):
        bucket = cls.get_bucket()
        image = BucketProductImage(
            bucket_id=bucket._id,
            image=file
        )
        if not idx:
            new_bucket = TemporaryPhotosBucket.query.find_and_modify(
                {'_id': bucket._id},
                update={'$push': {f'photos': image._id}},
                new=True,
            )
            print(f'pushed: {new_bucket}')
        else:
            new_bucket = TemporaryPhotosBucket.query.find_and_modify(
                {'_id': bucket._id},
                update={'$set': {f'photos.{idx}': image._id}},
                new=True,
            )
            print(f'set at idx {idx}: {new_bucket}')

        # app_model.DBSession.flush_all()
        # if I load them here they're in unit of work correctely
        # I mean, when you use find you can load them now and if you're just creating a product it seems to work
        # actually it was an ugly hack to load the lazy property immediatly
        # bucket.photos_rel

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


