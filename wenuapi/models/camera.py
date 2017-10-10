import requests

from .common import CommonColumns
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from io import BytesIO


class CameraException(Exception):
    """
        unable to capture an image from the camera
    """


class Camera(CommonColumns):
    __tablename__ = 'camera'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(String(80), nullable=False, unique=True)

    resolution = Column(String(80), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)

    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'camera'
    }

    def get_photo(self):
        """
            Should return image contents as a file like object,
            may return a CameraException when is not posible to obtain a capture
            :return: file_like, mimetype, filename
        """
        raise NotImplementedError


class BasicIPCamera(Camera):
    """
        camera format shuld be streamed in mjpg
    """
    url = Column(String(300))

    __mapper_args__ = {
        'polymorphic_identity': 'BasicIPCamera'
    }

    def get_photo(self):
        try:
            r = requests.get(self.url, stream=True, timeout=20)
        except requests.RequestException:
            raise CameraException

        if r.status_code == 200:
            bytes_data = bytes()
            for chunk in r.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b + 2]
                    bytes_data = bytes_data[b + 2:]
                    f = BytesIO()
                    f.write(jpg)
                    f.seek(0)
                    return f, "image/jpeg", "photo.jpg"
                    # with open("test.jpg", "wb") as f:
                    #     f.write(jpg)

        raise CameraException

