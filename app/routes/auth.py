from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.models.usuario import Usuario


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/")
def index():

    if current_user.is_authenticated:
        return redirect(
            url_for("dashboard.dashboard")
        )

    return redirect(
        url_for("auth.login")
    )


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        if (
            usuario and
            usuario.check_senha(senha) and
            usuario.ativo
        ):
            login_user(usuario)

            return redirect(
                url_for(
                    "dashboard.dashboard"
                )
            )

        flash(
            "E-mail ou senha inválidos.",
            "erro"
        )

    return render_template(
        "login.html"
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("auth.login")
    )


from app import db
from app.models.empresa import Empresa
from app.models.usuario import Usuario


@auth_bp.route("/criar-admin")
def criar_admin():

    usuario_existente = Usuario.query.filter_by(
        email="admin@mauntepix.com"
    ).first()

    if usuario_existente:
        return "Admin já existe."

    empresa = Empresa(
        nome="MauntePix",
        email="admin@mauntepix.com"
    )

    db.session.add(empresa)
    db.session.flush()

    usuario = Usuario(
        nome="Administrador",
        email="admin@mauntepix.com",
        perfil="admin",
        ativo=True,
        empresa_id=empresa.id
    )

    usuario.set_senha("123456")

    db.session.add(usuario)
    db.session.commit()

    return "Admin criado: admin@mauntepix.com / 123456"