from app import create_app, db
import uuid

app = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        try:
            conn.exec_driver_sql("ALTER TABLE clientes ADD COLUMN token_portal VARCHAR(120)")
            print("Coluna token_portal criada.")
        except Exception as e:
            print("token_portal:", e)

        conn.commit()

    from app.models.cliente_devedor import Cliente

    clientes = Cliente.query.all()

    for cliente in clientes:
        if not cliente.token_portal:
            cliente.token_portal = str(uuid.uuid4())

    db.session.commit()

print("Tokens dos clientes atualizados.")