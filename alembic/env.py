import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
import app.models

# Load all models so Alembic detects the complete schema
from app.models import user
from app.models import auth
from app.models import mining_site
from app.models import finance
from app.models import commission
from app.models import operations
from app.models import marketplace
from app.models import subscription

def include_object(object, name, type_, reflected, compare_to):
    ignored_tables = {
        'asset_items',
        'invoice',
        'escrow',
        'mining_assets',
    }

    # Prevent Alembic from generating destructive DROP operations
    if type_ == 'table' and reflected and compare_to is None:
        return False

    if type_ == 'table' and name in ignored_tables:
        return False

    return True

target_metadata = Base.metadata
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def get_url():
    return os.getenv('DATABASE_URL', config.get_main_option('sqlalchemy.url'))

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(render_as_batch=True,url=url, target_metadata=target_metadata, literal_binds=True, include_object=include_object)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration['sqlalchemy.url'] = get_url()
    connectable = engine_from_config(configuration, prefix='sqlalchemy.', poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(render_as_batch=True,connection=connection, target_metadata=target_metadata, include_object=include_object)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
