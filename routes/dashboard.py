from flask import Blueprint, render_template
from flask_login import login_required


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

    return render_template("dashboard.html")
from utils.decorators import role_required


@dashboard_bp.route("/recruiter-test")
@role_required("recruiter")
def recruiter_test():

    return "Recruiter access granted!"