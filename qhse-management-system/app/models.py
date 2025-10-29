from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from datetime import datetime

user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=True,  nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50), default='Employee')  # Admin, HSE, Supervisor, Employee, Auditor
    roles = db.relationship("Role", secondary=user_roles, backref=db.backref("users", lazy="dynamic"))
    is_active = db.Column(db.Boolean, default=True)     # email confirmed
    twofa_secret = db.Column(db.String(32), nullable=True) # optional TOTP secret

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_sec=3600, purpose='confirm'):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id, 'purpose': purpose})
    
    def has_role(self, role_name):
        return any(r.name == role_name for r in self.roles)

    def __repr__(self):
        return f"<User {self.full_name} - {self.email}>"
    
    def get_id(self):
        return str(self.id)  # Ensure this returns a string

    @staticmethod
    def verify_token(token, max_age=3600, purpose='confirm'):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=max_age)
        except Exception:
            return None
        if data.get('purpose') != purpose:
            return None
        return User.query.get(data.get('user_id'))


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Role {self.name}>"
    
class Incident(db.Model):
    __tablename__ = "incidents"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(128))
    type = db.Column(db.String(64))
    description = db.Column(db.Text)
    severity = db.Column(db.String(32))
    status = db.Column(db.String(32), default="Reported")  # e.g., Reported, Under Investigation, Resolved, Closed
    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_by = db.relationship("User", backref=db.backref("incidents", lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    incident_datetime = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "department": self.department,
            "type": self.type,
            "severity": self.severity,
            "status": self.status,
            "created_by": self.created_by.username if self.created_by else None,
            "created_at": self.created_at.isoformat(),
        }
        
class IncidentUpdate(db.Model):
    __tablename__ = "incident_updates"
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incidents.id"))
    incident = db.relationship("Incident", backref=db.backref("updates", lazy=True))
    update_text = db.Column(db.Text, nullable=False)
    updated_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated_by = db.relationship("User", backref=db.backref("incident_updates", lazy=True))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<IncidentUpdate {self.id} for Incident {self.incident_id}>"
    
class Capa(db.Model):
    __tablename__ = "capas"
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incidents.id"), nullable=True)
    incident = db.relationship("Incident", backref=db.backref("capas", lazy=True))
    action = db.Column(db.String(500))
    owner = db.Column(db.String(255))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(64), default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    uploaded_by = db.relationship("User")
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Audit(db.Model):
    __tablename__ = "audits"
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(255))
    standard = db.Column(db.String(255))
    plan_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
@login.user_loader
def load_user(user_id):
    print(f"🔍 Loading user with ID: {user_id}")  # Debug
    return User.query.get(int(user_id))
    print(f"🔍 User loaded: {user}")  # Debug
    return user



