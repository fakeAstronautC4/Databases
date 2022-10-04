
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import Length, DataRequired



class TeamForm(FlaskForm):
    
    team_name = StringField("Team Name", validators=[DataRequired(), Length(min=4, max=255)])
    user_id = FloatField('User ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProjectForm(FlaskForm):

    project_name = StringField("Project Name", validators=[DataRequired(), Length(min=4, max=255)]) 
    description = StringField("Description", validators=[DataRequired(), Length(min=4, max=255)])
    completed = SelectField("Completed?", choices=[('True', 'True'), ('False', 'False')])
    team_id = FloatField('Team ID', validators=[DataRequired()])
    submit = SubmitField("Submit")

class TeamSearch(FlaskForm):

    team3_name = StringField("Team Name", validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField('Submit')