import uuid

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.cliente_devedor import Cliente

clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.route("/clientes")
@login_required
def listar_clientes():
    lista = Cliente.query.filter_by(
        empresa_id=current_user.empresa_id
    ).order_by(Cliente.id.desc()).all()

    for cliente in lista:
        if not cliente.token_portal:
            cliente.token_portal = str(uuid.uuid4())

    db.session.commit()

    return render_template("clientes.html", clientes=lista)


@clientes_bp.route("/clientes/novo", methods=["GET", "POST"])
@login_required
def novo_cliente():
    if request.method == "POST":
        cliente = Cliente(
            empresa_id=current_user.empresa_id,
            nome=request.form.get("nome"),
            cpf=request.form.get("cpf"),
            rg=request.form.get("rg"),
            telefone=request.form.get("telefone"),
            whatsapp=request.form.get("whatsapp"),
            email=request.form.get("email"),
            cep=request.form.get("cep"),
            logradouro=request.form.get("logradouro"),
            numero=request.form.get("numero"),
            complemento=request.form.get("complemento"),
            bairro=request.form.get("bairro"),
            cidade=request.form.get("cidade"),
            estado=request.form.get("estado"),
            endereco=request.form.get("endereco"),
            token_portal=str(uuid.uuid4())
        )

        db.session.add(cliente)
        db.session.commit()

        flash("Cliente cadastrado com sucesso!", "sucesso")
        return redirect(url_for("clientes.listar_clientes"))

    return render_template("cliente_form.html", cliente=None)


@clientes_bp.route("/clientes/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.filter_by(
        id=id,
        empresa_id=current_user.empresa_id
    ).first_or_404()

    if not cliente.token_portal:
        cliente.token_portal = str(uuid.uuid4())
        db.session.commit()

    if request.method == "POST":
        cliente.nome = request.form.get("nome")
        cliente.cpf = request.form.get("cpf")
        cliente.rg = request.form.get("rg")
        cliente.telefone = request.form.get("telefone")
        cliente.whatsapp = request.form.get("whatsapp")
        cliente.email = request.form.get("email")
        cliente.cep = request.form.get("cep")
        cliente.logradouro = request.form.get("logradouro")
        cliente.numero = request.form.get("numero")
        cliente.complemento = request.form.get("complemento")
        cliente.bairro = request.form.get("bairro")
        cliente.cidade = request.form.get("cidade")
        cliente.estado = request.form.get("estado")
        cliente.endereco = request.form.get("endereco")

        db.session.commit()

        flash("Cliente atualizado com sucesso!", "sucesso")
        return redirect(url_for("clientes.listar_clientes"))

    return render_template("cliente_form.html", cliente=cliente)


@clientes_bp.route("/clientes/<int:id>/excluir")
@login_required
def excluir_cliente(id):
    cliente = Cliente.query.filter_by(
        id=id,
        empresa_id=current_user.empresa_id
    ).first_or_404()

    db.session.delete(cliente)
    db.session.commit()

    flash("Cliente excluído com sucesso!", "sucesso")
    return redirect(url_for("clientes.listar_clientes"))