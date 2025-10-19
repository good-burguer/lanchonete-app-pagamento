import os
import re
import json
import sqlalchemy as sa
from alembic import context
from urllib.parse import quote_plus

# Tentativa de import do Base da aplicação para suportar autogenerate
try:
    from app.db import Base  # ajuste se necessário
    target_metadata = Base.metadata
except Exception:
    target_metadata = None

config = context.config


def _mask(u: str) -> str:
    try:
        return re.sub(r"://([^:/@]+):([^@]+)@", r"://\1:***@", u)
    except Exception:
        return u


def _with_sslmode(url: str) -> str:
    if "sslmode=" in url:
        return url
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}sslmode=require"


def _from_secrets_manager() -> str:
    """Constroi uma URL lendo credenciais do AWS Secrets Manager.
    Requer DB_SECRET_NAME e (AWS_REGION ou AWS_DEFAULT_REGION).
    Retorna string vazia se não conseguir resolver.
    """
    name = os.getenv("DB_SECRET_NAME", "").strip()
    if not name:
        return ""

    region = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "")).strip()
    if not region:
        # sem região, não dá para consultar o SM
        return ""

    try:
        import boto3  # disponível na imagem da app
        sm = boto3.client("secretsmanager", region_name=region)
        raw = sm.get_secret_value(SecretId=name)["SecretString"]
        data = json.loads(raw)
        host = data.get("host") or data.get("hostname")
        port = int(data.get("port", 5432))
        db   = data.get("dbname") or data.get("database")
        user = data.get("username") or data.get("user")
        pwd  = data.get("password") or data.get("pwd")
        if not all([host, db, user, pwd]):
            return ""
        # URL-encode na senha para caracteres especiais
        pwd_q = quote_plus(pwd)
        url = f"postgresql+psycopg2://{user}:{pwd_q}@{host}:{port}/{db}"
        print(f"[alembic] Using DB URL source=secretsmanager({name}): {_mask(url)}")
        return _with_sslmode(url)
    except Exception as e:
        print(f"[alembic] secretsmanager error: {type(e).__name__}")
        return ""


def _build_db_url() -> str:
    """Tenta importar um helper do projeto; se não existir, retorna string vazia."""
    try:
        from app.settings import build_db_url as _b
        return _b()
    except Exception:
        return ""


def _get_db_url() -> str:
    """
    Ordem de resolução:
      1) ALEMBIC_DATABASE_URL
      2) DATABASE_URL
      3) Segredo no Secrets Manager (DB_SECRET_NAME)
      4) Helper do projeto (_build_db_url)
      5) sqlalchemy.url do alembic.ini
    Sempre força sslmode=require quando não especificado.
    """
    # 1) ALEMBIC_DATABASE_URL
    env_alembic = os.getenv("ALEMBIC_DATABASE_URL", "").strip()
    if env_alembic:
        print(f"[alembic] Using DB URL source=env(ALEMBIC_DATABASE_URL): {_mask(env_alembic)}")
        return _with_sslmode(env_alembic)

    # 2) DATABASE_URL
    env_database = os.getenv("DATABASE_URL", "").strip()
    if env_database:
        print(f"[alembic] Using DB URL source=env(DATABASE_URL): {_mask(env_database)}")
        return _with_sslmode(env_database)

    # 3) AWS Secrets Manager
    sm_url = _from_secrets_manager()
    if sm_url:
        return sm_url

    # 4) Helper do projeto
    try:
        built_url = _build_db_url()
        if built_url:
            print(f"[alembic] Using DB URL source=build_url: {_mask(built_url)}")
            return _with_sslmode(built_url)
    except Exception as e:
        print(f"[alembic] _build_db_url() falhou: {type(e).__name__}")

    # 5) alembic.ini
    ini_url = config.get_main_option("sqlalchemy.url")
    if ini_url:
        print(f"[alembic] Using DB URL source=ini: {_mask(ini_url)}")
        return _with_sslmode(ini_url)

    raise RuntimeError(
        "Nenhuma URL de banco encontrada. Defina ALEMBIC_DATABASE_URL ou DATABASE_URL, "
        "ou exponha DB_SECRET_NAME (com AWS_REGION/AWS_DEFAULT_REGION), ou configure sqlalchemy.url no alembic.ini."
    )


def run_migrations_offline() -> None:
    url = _get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = sa.create_engine(_get_db_url())
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()