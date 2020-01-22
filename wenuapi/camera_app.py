from flask import (
    current_app as app,
    Response,
    send_file
)
from sqlalchemy.orm.exc import NoResultFound

from .models.camera import Camera


def get_camera_photo(camera_id):
    '''Returns a Flask response containing a frame of the selected camera'''
    session = app.data.driver.session
    try:
        camera = session.query(Camera).filter(Camera.camera_id == camera_id).one()
    except NoResultFound:
        return "", 404

    # TODO handle CameraException properly
    # Grabs a file like object with a new frame from the selected camera
    file_like, mimetype, filename = camera.get_photo()

    # Returns a response with the retrieved frame
    return send_file(
        file_like,
        mimetype=mimetype,
        as_attachment=False,
        attachment_filename=filename
    )


def init_camera_app(app):
    '''Setups a route to fetch images of a camera monitoring a particular room,
    each camera has an identifying id'''
    app.route('/photo/<string:camera_id>', methods=['GET'])(get_camera_photo)
