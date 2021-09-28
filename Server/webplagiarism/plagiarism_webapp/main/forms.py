from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField
from wtforms.validators import ValidationError
import os


class UploadSongsForm(FlaskForm):
    song_file1 = FileField('First Song', validators=[FileRequired(), FileAllowed(['xml'])])
    song_file2 = FileField('Second Song', validators=[FileRequired(), FileAllowed(['xml'])])
    submit = SubmitField('Upload and check')

    def validate_song_file2(self, song_file2):
        song1_name, _ = os.path.splitext(self.song_file1.data.filename)  # prendiamo la variabile con self !
        song2_name, _ = os.path.splitext(song_file2.data.filename)
        if song1_name == song2_name:
            raise ValidationError('You cannot upload the same song twice.')
