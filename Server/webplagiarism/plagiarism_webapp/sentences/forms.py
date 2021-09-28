from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField  # importato radiofield per test
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired
import os


class SentenceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=60)])
    first_song = StringField('First Song', validators=[DataRequired()])  #
    second_song = StringField('Second Song', validators=[DataRequired()])  #
    info = TextAreaField('Info', validators=[DataRequired(), Length(min=2, max=5000)])
    radio_choice = RadioField('Status', choices=[('noTrial', 'Not In Trial'),
                                                 ('hasTrial', 'In Trial'),
                                                 ('hasTrialAndVerdict', 'Went in Trial and has Verdict')],
                              default='noTrial', validators=[DataRequired()])
    verdict_file = FileField('Verdict', validators=[FileAllowed(['pdf'], 'PDFs only!')])
    submit = SubmitField('Post Case')


class SentenceWithFilesForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=60)])
    first_song = StringField('First Song', validators=[DataRequired()])  #
    second_song = StringField('Second Song', validators=[DataRequired()])  #
    song_file1 = FileField('First Song', validators=[FileRequired(), FileAllowed(['xml'])])
    song_file2 = FileField('Second Song', validators=[FileRequired(), FileAllowed(['xml'])])
    info = TextAreaField('Info', validators=[DataRequired(), Length(min=2, max=5000)])
    radio_choice = RadioField('Status', choices=[('noTrial', 'Not In Trial'),
                                                 ('hasTrial', 'In Trial'),
                                                 ('hasTrialAndVerdict', 'Went in Trial and has Verdict')],
                              default='noTrial', validators=[DataRequired()])
    verdict_file = FileField('Verdict', validators=[FileAllowed(['pdf'], 'PDFs only!')])
    submit = SubmitField('Post Case')

    def validate_song_file2(self, song_file2):
        song1_name, _ = os.path.splitext(self.song_file1.data.filename)  # prendiamo la variabile con self !
        song2_name, _ = os.path.splitext(song_file2.data.filename)
        if song1_name == song2_name:
            raise ValidationError('You cannot upload the same song twice.')


class UpdateSentenceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=60)])
    first_song = StringField('First Song', validators=[DataRequired()])  #
    second_song = StringField('Second Song', validators=[DataRequired()])  #
    song_file1 = FileField('First Song', validators=[FileAllowed(['xml'])])  # in questo caso non sono obbligatori
    song_file2 = FileField('Second Song', validators=[FileAllowed(['xml'])])
    info = TextAreaField('Info', validators=[DataRequired(), Length(min=2, max=5000)])
    radio_choice = RadioField('Status',
                              choices=[('noTrial', 'Not In Trial'),
                                       ('hasTrial', 'In Trial'),
                                       ('hasTrialAndVerdict',
                                        'Went in Trial and has Verdict [If case has a pdf file already leave blank.]')],
                              default='noTrial', validators=[DataRequired()])
    verdict_file = FileField('Verdict', validators=[FileAllowed(['pdf'], 'PDFs only!')])
    submit = SubmitField('Update Case')

    def validate_song_file2(self, song_file2):
        if song_file2.data and self.song_file1.data:  # se esiste song1name fai il controllo, sennò non fare nulla
            song1_name, _ = os.path.splitext(self.song_file1.data.filename)  # prendiamo la variabile con self !
            song2_name, _ = os.path.splitext(song_file2.data.filename)
            if song1_name == song2_name:
                raise ValidationError('You cannot upload the same song twice.')


class SearchForm(FlaskForm):
    search_titles = StringField("Title")  # Ricerca nei titoli delle canzoni e nel titolo del caso
    search_author = StringField("Author")  # Ricerca autore (nel titolo "autore vs autore")
    search_info = StringField("Info")  # Ricerca infp
    submit = SubmitField('Search')
