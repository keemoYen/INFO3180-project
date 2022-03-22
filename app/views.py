"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from werkzeug.utils import secure_filename
from fileinput import filename
from app import app, db
from flask import render_template, request, redirect, url_for, flash,session, abort, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, PropertyForm
from app.models import UserProfile,property
import os
from werkzeug.security import check_password_hash


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/secure-page')
@login_required
def secure_page():
    return render_template('secure_page.html')


@app.route('/create',methods=["GET","POST"])
def create_property():
    form = PropertyForm()
    if request.method == "POST":
        
        if form.validate_on_submit():
            title=form.p_title.data
            description=form.description.data
            location=form.location.data
            no_bedrooms=form.number_bedrooms.data
            no_bathrooms=form.number_bathrooms.data
            price=form.price.data
            type=form.property_type.data
            
            photo=request.files['photo']
            
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            

            print(photo)

            property1 = property(title,description,no_bedrooms,no_bathrooms,price,location,type,filename)
            db.session.add(property1)
            db.session.commit()
            

    return render_template("new_property_form.html", form=form)


###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')



def get_upload_images():
    rootdir = os.getcwd()
    lst=[]
    for subdir, dirs, files in os.walk(rootdir + '\\upload'):
        for file in files:
            lst.append(os.path.join(file))
    print(lst)
    return lst


@app.route("/uploads/<filename>")
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

@app.route('/properties')
def properties():
    property_list = db.session.query(property).all()
    return render_template("property_list.html",lst=property_list)

@app.route('/property/<id>')
def view_property(id):
    prop = property.query.get(id)
    print(prop.photo)
    return(render_template('property.html',p1blue=prop))

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")