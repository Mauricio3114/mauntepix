from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.usuario import Usuario


usuarios_bp = Blueprint("usuarios", __name__)


def somente_admin():
    return current_user.is_authenticated and current_user.perfil in ["master", "admin"]


def perfil_permitido(perfil):
    if current_user.perfil == "master":
        return perfil in ["master", "admin", "operador", "consulta"]

    return perfil in ["admin", "operador", "consulta"]


def query_usuarios_empresa():
    return Usuario.query.filter_by(
        empresa_id=current_user.empresa_id
    )


@usuarios_bp.route("/usuarios")
@login_required
def listar_usuarios():
    if not somente_admin():
        flash("Você não tem permissão para acessar usuários.", "erro")
        return redirect(url_for("dashboard.dashboard"))

    usuarios = query_usuarios_empresa().order_by(Usuario.nome.asc()).all()

    return render_template("usuarios.html", usuarios=usuarios)


@usuarios_bp.route("/usuarios/novo", methods=["GET", "POST"])
@login_required
def novo_usuario():
    if not somente_admin():
        flash("Você não tem permissão para cadastrar usuários.", "erro")
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        perfil = request.form.get("perfil", "operador")

        if not nome or not email or not senha:
            flash("Preencha nome, e-mail e senha.", "erro")
            return redirect(url_for("usuarios.novo_usuario"))

        if not perfil_permitido(perfil):
            flash("Perfil não permitido para seu usuário.", "erro")
            return redirect(url_for("usuarios.novo_usuario"))

        existe = Usuario.query.filter_by(email=email).first()

        if existe:
            flash("Já existe um usuário com esse e-mail.", "erro")
            return redirect(url_for("usuarios.novo_usuario"))

        usuario = Usuario(
            empresa_id=current_user.empresa_id,
            nome=nome,
            email=email,
            perfil=perfil,
            ativo=True
        )

        usuario.set_senha(senha)

        db.session.add(usuario)
        db.session.commit()

        flash("Usuário cadastrado com sucesso.", "sucesso")
        return redirect(url_for("usuarios.listar_usuarios"))

    return render_template("usuario_form.html", usuario=None)


@usuarios_bp.route("/usuarios/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_usuario(id):
    if not somente_admin():
        flash("Você não tem permissão para editar usuários.", "erro")
        return redirect(url_for("dashboard.dashboard"))

    usuario = query_usuarios_empresa().filter_by(id=id).first_or_404()

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        perfil = request.form.get("perfil", "operador")
        senha = request.form.get("senha")

        if not perfil_permitido(perfil):
            flash("Perfil não permitido para seu usuário.", "erro")
            return redirect(url_for("usuarios.editar_usuario", id=id))

        if usuario.id == current_user.id and perfil != current_user.perfil:
            flash("Você não pode alterar seu próprio perfil.", "erro")
            return redirect(url_for("usuarios.editar_usuario", id=id))

        email_existente = Usuario.query.filter(
            Usuario.email == email,
            Usuario.id != usuario.id
        ).first()

        if email_existente:
            flash("Já existe outro usuário com esse e-mail.", "erro")
            return redirect(url_for("usuarios.editar_usuario", id=id))

        usuario.nome = nome
        usuario.email = email
        usuario.perfil = perfil

        if senha:
            usuario.set_senha(senha)

        db.session.commit()

        flash("Usuário atualizado com sucesso.", "sucesso")
        return redirect(url_for("usuarios.listar_usuarios"))

    return render_template("usuario_form.html", usuario=usuario)


@usuarios_bp.route("/usuarios/<int:id>/status")
@login_required
def alterar_status_usuario(id):
    if not somente_admin():
        flash("Você não tem permissão para alterar usuários.", "erro")
        return redirect(url_for("dashboard.dashboard"))

    usuario = query_usuarios_empresa().filter_by(id=id).first_or_404()

    if usuario.id == current_user.id:
        flash("Você não pode inativar seu próprio usuário.", "erro")
        return redirect(url_for("usuarios.listar_usuarios"))

    if usuario.perfil == "master" and current_user.perfil != "master":
        flash("Você não pode alterar um usuário master.", "erro")
        return redirect(url_for("usuarios.listar_usuarios"))

    usuario.ativo = not usuario.ativo

    db.session.commit()

    flash("Status do usuário alterado com sucesso.", "sucesso")
    return redirect(url_for("usuarios.listar_usuarios"))