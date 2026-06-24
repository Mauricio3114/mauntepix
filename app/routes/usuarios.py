from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.usuario import Usuario


usuarios_bp = Blueprint("usuarios", __name__)


def somente_admin():
    return current_user.is_authenticated and current_user.is_admin()


@usuarios_bp.route("/usuarios")
@login_required
def listar_usuarios():
    if not somente_admin():
        flash("Você não tem permissão para acessar usuários.", "erro")
        return redirect(url_for("dashboard.dashboard"))

    usuarios = Usuario.query.filter_by(
        empresa_id=current_user.empresa_id
    ).order_by(Usuario.nome.asc()).all()

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

    usuario = Usuario.query.filter_by(
        id=id,
        empresa_id=current_user.empresa_id
    ).first_or_404()

    if request.method == "POST":
        usuario.nome = request.form.get("nome")
        usuario.email = request.form.get("email")
        usuario.perfil = request.form.get("perfil", "operador")

        senha = request.form.get("senha")

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

    usuario = Usuario.query.filter_by(
        id=id,
        empresa_id=current_user.empresa_id
    ).first_or_404()

    if usuario.id == current_user.id:
        flash("Você não pode inativar seu próprio usuário.", "erro")
        return redirect(url_for("usuarios.listar_usuarios"))

    usuario.ativo = not usuario.ativo

    db.session.commit()

    flash("Status do usuário alterado com sucesso.", "sucesso")
    return redirect(url_for("usuarios.listar_usuarios"))