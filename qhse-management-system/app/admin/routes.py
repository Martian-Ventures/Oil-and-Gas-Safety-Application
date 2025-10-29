from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import User, Role
from app.decorators import role_required

admin_bp = Blueprint("admin", __name__, template_folder="../templates")

@admin_bp.route("/users")
@role_required("Admin")
def manage_users():
    users = User.query.all()
    roles = Role.query.all()
    return render_template("admin_users.html", users=users, roles=roles)

@admin_bp.route("/users/<int:user_id>/assign", methods=["POST"])
@role_required("Admin")
def assign_role(user_id):
    user = User.query.get_or_404(user_id)
    role_id = request.form.get("role_id")
    role = Role.query.get(role_id)
    if role and role not in user.roles:
        user.roles.append(role)
        db.session.commit()
        flash(f"Assigned role {role.name} to {user.full_name}", "success")
    return redirect(url_for("admin.manage_users"))
