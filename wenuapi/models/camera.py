import requests

from .common import CommonColumns
from sqlalchemy import (
    Column,
    Integer,
    String,
)

from io import BytesIO


class Camera(CommonColumns):
    __tablename__ = 'camera'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(String(80), nullable=False, unique=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    url = Column(String(200))

    def get_photo(self):
        """
            Should return image contents as a file like object
            :return: file_like, mimetype, filename
        """
        r = requests.get(self.url, auth=('hackme', 'hackme'), stream=True)
        if (r.status_code == 200):
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
