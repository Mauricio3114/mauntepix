from app import db


class ConfigPix(db.Model):
    __tablename__ = "config_pix"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    chave_pix = db.Column(db.String(200))

    public_key = db.Column(db.Text)

    access_token = db.Column(db.Text)

    ativo = db.Column(db.Boolean, default=True)

    empresa = db.relationship("Empresa", backref="config_pix")