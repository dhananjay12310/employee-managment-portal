from main import app , login_manager
from flask import render_template , redirect , url_for, flash , request
from main.models import emp_info
from main.forms import empRegForm , admin_login_form , employee_login_form
from main import db
from flask_login import login_user , logout_user , login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/employee_master')
@login_required
def employee_master_page():

    q= request.args.get('q')
    if q:
        Emp_info = emp_info.query.filter(emp_info.first_name.contains(q) |
                                         emp_info.address.contains(q))
    else:
        Emp_info = emp_info.query.all()

    return render_template('employee_master.html', emp_info=Emp_info)




@app.route('/empRegister', methods=['GET','POST'])
@login_required
def empRegister_page():
    form= empRegForm()

    if form.validate_on_submit():
        emp_to_create = emp_info(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     email= form.email.data,
                     phone= form.phone.data,
                     dob= form.dob.data,
                     address=form.address.data,
                     password=form.password.data,
                     admin=form.admin.data)
        db.session.add(emp_to_create)
        db.session.commit()
        return redirect(url_for('employee_master_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'erore with creating a user: {err_msg}', category='danger')

    return render_template('empRegister.html',form=form)

@app.route('/admin_login', methods=['GET','POST'])
def admin_login_page():
    form = admin_login_form()
    if form.validate_on_submit():
        attempted_user = emp_info.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data) and attempted_user.check_admin():
            login_user(attempted_user)
            # flash(f'success! you are now logged in as: {attempted_user.email}', category='success')
            return redirect(url_for('employee_master_page'))

        else:
            flash('email and password did not match! please try again', category='danger')


    return render_template('admin_login.html', form=form)

@app.route('/employee_detail')
@login_required
def employee_detail_page():
    Emp_info = emp_info.query.all()

    return render_template('employee_detail.html', emp_info=Emp_info)

@app.route('/employee_login', methods=['GET','POST'])
def employee_login_page():
    form=employee_login_form()
    if form.validate_on_submit():
        attempted_user = emp_info.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            # flash(f'success! you are now logged in as: {attempted_user.email}', category='success')
            return redirect(url_for('employee_detail_page'))

        else:
            flash('email and password did not match! please try again', category='danger')

    return render_template('emp_login.html', form=form)






@app.route('/logout')
def logout_page():
    logout_user()
    flash("success! logged out",category='info')
    return redirect(url_for('home_page'))



