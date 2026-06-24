from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.solicitacao_negociacao import SolicitacaoNegociacao
from app.models.cliente_devedor import Cliente


negociacoes_bp = Blueprint("negociacoes", __name__)


@negociacoes_bp.route("/portal/<token>/negociar", methods=["GET", "POST"])
def negociar_cliente(token):
    cliente = Cliente.query.filter_by(token_portal=token, ativo=True).first_or_404()

    if request.method == "POST":
        solicitacao = SolicitacaoNegociacao(
            empresa_id=cliente.empresa_id,
            cliente_id=cliente.id,
            tipo=request.form.get("tipo"),
            valor=request.form.get("valor") or 0,
            observacao=request.form.get("observacao"),
            status="pendente"
        )

        db.session.add(solicitacao)
        db.session.commit()

        return render_template("negociacao_enviada.html", cliente=cliente)

    return render_template("negociar_cliente.html", cliente=cliente)


@negociacoes_bp.route("/negociacoes")
@login_required
def listar_negociacoes():
    solicitacoes = SolicitacaoNegociacao.query.filter_by(
        empresa_id=current_user.empresa_id
    ).order_by(SolicitacaoNegociacao.id.desc()).all()

    return render_template("negociacoes.html", solicitacoes=solicitacoes)


@negociacoes_bp.route("/negociacoes/<int:id>")
@login_required
def detalhes_negociacao(id):

    solicitacao = SolicitacaoNegociacao.query.filter_by(
        id=id,
        empresa_id=current_user.empresa_id
    ).first_or_404()

    return render_template(
        "negociacao_detalhes.html",
        solicitacao=solicitacao
    )


@negociacoes_bp.route("/negociacoes/<int:id>/concluir")
@login_required
def concluir_negociacao(id):
    solicitacao = SolicitacaoNegociacao.query.filter_by(
        id=id,
        empresa_id=current_user.empresa_id
    ).first_or_404()

    solicitacao.status = "concluida"
    db.session.commit()

    flash("Negociação marcada como concluída.", "sucesso")
    return redirect(url_for("negociacoes.listar_negociacoes"))