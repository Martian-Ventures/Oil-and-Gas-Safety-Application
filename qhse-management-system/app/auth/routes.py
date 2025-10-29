from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from .. import db, mail
from ..models import User, Role
from .forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm

# Create the auth blueprint - THIS LINE MUST EXIST
bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User(full_name=form.full_name.data, email=form.email.data)
        user.set_password(form.password.data)
        
        employee_role = Role.query.filter_by(name="Employee").first()
        if employee_role:
            user.roles.append(employee_role)
            
        db.session.add(user)
        db.session.commit()

        token = user.get_token(purpose='confirm')
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        msg = Message('Confirm your account', recipients=[user.email])
        msg.body = f'Please confirm your account: {confirm_url}'
        mail.send(msg)

        flash('Registration successful. Check your email to confirm your account.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/confirm/<token>')
def confirm_email(token):
    user = User.verify_token(token, purpose='confirm')
    if not user:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))
    
    user.is_active = True
    db.session.commit()
    flash('Email confirmed! You can now log in.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        print("✅ User already authenticated, redirecting to dashboard")
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        print("✅ Form validation passed")
        user = User.query.filter_by(email=form.email.data).first()
        print(f"🔍 User found: {user}")
        
        if user is None or not user.check_password(form.password.data):
            print("❌ Invalid credentials")
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))

        print(f"🔍 User active status: {user.is_active}")
        
        # Login the user
        login_user(user, remember=form.remember_me.data)
        
        # IMPORTANT: Commit the session to ensure it's saved
        from flask import session
        session.modified = True
        
        print(f"🔍 Session after login: {dict(session)}")
        print(f"🔍 Current user authenticated: {current_user.is_authenticated}")
        print(f"🔍 Current user ID: {current_user.get_id()}")
        
        flash('Logged in successfully.', 'success')
        next_page = request.args.get('next')
        print(f"✅ Redirecting to: {next_page or 'dashboard'}")
        
        # Create the response manually to ensure session is committed
        response = redirect(next_page or url_for('main.dashboard'))
        return response
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.get_token(purpose='reset')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message('Password Reset', recipients=[user.email])
            msg.body = f'Reset your password: {reset_url}'
            mail.send(msg)
        
        flash('If an account with that email exists, we sent a reset email.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_request.html', form=form)

@bp.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    user = User.verify_token(token, purpose='reset')
    if not user:
        flash('Invalid or expired token', 'danger')
        return redirect(url_for('auth.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)