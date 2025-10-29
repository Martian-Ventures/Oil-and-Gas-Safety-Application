from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Incident
from datetime import datetime

incidents_bp = Blueprint("incidents", __name__, template_folder="../templates")

@incidents_bp.route("/list")
@login_required
def list_incidents():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return jsonify([i.to_dict() for i in incidents])

@incidents_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_incident():
    if request.method == "POST":
        inc = Incident(
            title=request.form["title"],
            department=request.form["department"],
            type=request.form["type"],
            description=request.form["description"],
            incident_datetime=datetime.now(),
            created_by=current_user,
        )
        db.session.add(inc)
        db.session.commit()
        flash("Incident created.", "success")
        return redirect(url_for("incidents.list_incidents"))
    return render_template("new_incident.html")

@incidents_bp.route("/<int:incident_id>")
@login_required
def view_incident(incident_id):
    inc = Incident.query.get_or_404(incident_id)
    return render_template("incident_detail.html", incident=inc)
