from flask import (
    current_app as app,
    Response,
    send_file
)
from sqlalchemy.orm.exc import NoResultFound

from .models.camera import Camera


def get_camera_photo(camera_id):
    session = app.data.driver.session
    try:
        camera = session.query(Camera).filter(Camera.camera_id == camera_id).one()
    except NoResultFound:
        return "", 404

    # TODO handle CameraException properly
    file_like, mimetype, filename = camera.get_photo()

    return send_file(
        file_like,
        mimetype=mimetype,
        as_attachment=False,
        attachment_filename=filename
    )


def init_camera_app(app):
    app.route('/photo/<string:camera_id>', methods=['GET'])(get_camera_photo)
