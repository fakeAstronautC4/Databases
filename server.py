
import os
import psycopg2
from flask import Flask, render_template, redirect, url_for
import requests
from forms import TeamForm, ProjectForm, TeamSearch 
import jinja2
from flask_sqlalchemy import SQLAlchemy
from model import Teams, User, Project, connect_to_db, db

app = Flask(__name__)
app.secret_key = 'mamawebassso'

############################################################################
connection=psycopg2.connect(user='alons',
                                password='hqO1451**Ken',
                                host='127.0.0.1',
                                database='project-tracking-app')

cursor = connection.cursor()
###############################################################################################

@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    find_team = TeamSearch()
    return render_template ("base.html", team_form=team_form, project_form=project_form, find_team = find_team)


###############################################################################################
@app.route("/add_team", methods=['POST'])
def add_team():
    team_form = TeamForm()
    if team_form.validate_on_submit():
        team1_name = team_form.team_name.data
        user_id = team_form.user_id.data
        new_team = Teams(str(team1_name), user_id) 
        db.session.add(new_team)
        db.session.commit()
        return redirect (url_for("home"))
    else:
        return redirect (url_for("home"))


###############################################################################################
@app.route("/add_project", methods=['POST'])
def add_project():
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        proj_name = project_form.project_name.data 
        proj_desc = project_form.description.data
        if project_form.completed.data == 'True':
            proj_status = True
        else:
            proj_status = False
        team_ref = project_form.team_id.data 

        new_proj = Project (proj_name, proj_desc, proj_status, team_ref)
        db.session.add(new_proj)
        db.session.commit()
        print()
        return redirect (url_for("home"))
    else:
        return redirect (url_for("home"))


###############################################################################################
@app.route("/show_all_teams", methods=['POST'])
def show_all_teams():
    find_team = TeamSearch()
    if find_team.validate_on_submit():
        team_input = find_team.team3_name.data
        team_obj = Teams.query.filter_by(team_name = team_input).first()
        if team_obj == None:
            print("Something")
            return render_template('404.html')
        name_to_send = team_obj.team_name
        id_to_send = team_obj.user_id
        return render_template('show_all_teams.html', name_to_send = name_to_send, id_to_send = id_to_send)
    else:
       return redirect (url_for("home"))


###############################################################################################
@app.route("/render_projects", methods=['GET'])
def project_table():
    
    postgreSQL_seles_Query = "select * from projects"
    cursor.execute(postgreSQL_seles_Query)
    all_projects = cursor.fetchall()
    
    return render_template ('render_projects.html', all_projects = all_projects)


###############################################################################################
# @app.route('/update_project')
# def update_project():
#     project_id = requests.get('values')
#     project = Project.query.filter_by(id = project_id).first()
#     print(project)
#     return render_template ('update_projects.html', project = project)


###############################################################################################
@app.errorhandler(404)
def notfound(e):
   return render_template('404.html')



###############################################################################################
if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)