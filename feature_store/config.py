import os
from feature_store.logger import Logger

log = Logger("config_loader").get_logger()

LOCAL_URL = "postgresql://postgres:mysecretpassword@localhost:5432/feature_store"
LOCAL_MONGO = 'mongodb://root:root@0.0.0.0:27017/admin'

if os.getenv("DB_SCHEMA"):
    SCHEMA = os.getenv("DB_SCHEMA")
else:
    raise ValueError("DB_SCHEMA env was not found")

if os.getenv("DATABASE_URL"):
    PSG_URL = os.getenv("DATABASE_URL")
else:
    log.warn("Using local email since DATABASE_URL env was not found")
    PSG_URL = LOCAL_URL

if os.getenv("MONGODB_URI"):
    MDB_URL = os.getenv("MONGODB_URI")
else:
    log.warn("Using local email since MONGO_URL env was not found")
    MDB_URL = LOCAL_MONGO

class CatalogConstants():
    catalog_collections = {
        "query": "query",
        "feature": "feature",
        "model": "model"
    }


class Schemas():
    SCHEMA = {
        "name": SCHEMA,
        "create": """CREATE SCHEMA IF NOT EXISTS {};""".format(SCHEMA)
    }

class Tables():
    USERS = {
        "name": "users",
        "create_rt": """
            create table if not exists main.Users (
                user_id VARCHAR(36),
                name TEXT NOT NULL,
                address TEXT,
                creation_date DECIMAL NOT NULL,
                PRIMARY KEY (user_id)
            );
        """,
        "create": """
            create table if not exists {schema}.Users (
                user_id VARCHAR(36),
                name TEXT NOT NULL,
                address TEXT,
                creation_date DECIMAL NOT NULL,
                PRIMARY KEY (user_id)
            );
        """.format(schema=SCHEMA),
        "insert": """
            INSERT INTO {schema}.Users (user_id, name, address, creation_date)
            VALUES (%(user_id)s::varchar(36), %(name)s::text, %(address)s::text, %(creation_date)s::decimal)
            ON CONFLICT (user_id) DO NOTHING
        """.format(schema=SCHEMA),
        "insert_rt": """
            INSERT INTO main.Users (user_id, name, address, creation_date)
            VALUES (?, ?, ?, ?)
        """,
        "rt_values": ["user_id", "name", "address", "creation_date"]
    }
    
   
    QUOTES = {
        "name": "Quotes",
        "create_rt": """
            create table if not exists main.Quotes (
                quote_id VARCHAR(36),
                user_id VARCHAR(36),
                creation_date DECIMAL NOT NULL,
                binding_date DECIMAL,
                quote_type TEXT,
                quote_device TEXT,
                is_binded BOOLEAN,
                is_paid BOOLEAN,
                CONSTRAINT PK_Quotes PRIMARY KEY (quote_id)
            );
        """,
        "create": """
            create table if not exists {schema}.Quotes (
                quote_id VARCHAR(36),
                user_id VARCHAR(36),
                creation_date DECIMAL NOT NULL,
                binding_date DECIMAL,
                quote_type TEXT,
                quote_device TEXT,
                is_binded BOOLEAN,
                is_paid BOOLEAN,
                PRIMARY KEY (quote_id)
            );
        """.format(schema=SCHEMA),
        "insert_rt": """
            INSERT INTO main.Quotes (quote_id, user_id, creation_date, binding_date, quote_type, quote_device, is_binded, is_paid)
            VALUES (?,?,?,?,?,?,?,?)
        """,
        "insert": """
            INSERT INTO {schema}.Quotes (quote_id, user_id, creation_date, binding_date, quote_type, quote_device, is_binded, is_paid)
            VALUES (%(quote_id)s::varchar(36), %(user_id)s::varchar(36), %(creation_date)s::decimal, %(binding_date)s::decimal, %(quote_type)s::text, %(quote_device)s::text, %(is_binded)s::boolean , %(is_paid)s::boolean)
        """.format(schema=SCHEMA),
        "rt_values": ["quote_id", "user_id", "creation_date", "binding_date", "quote_type", "quote_device", "is_binded", "is_paid"]
    }

    POLICIES = {
        "name": "Policies",
        "create_rt": """
            create table if not exists main.Policies (
                policy_id VARCHAR(36),
                user_id VARCHAR(36) NOT NULL,
                quote_id VARCHAR(36) NOT NULL,
                purchase_time DECIMAL NOT NULL,
                policy_type TEXT,
                policy_device TEXT,
                CONSTRAINT PK_Policies PRIMARY KEY (policy_id)
            );
        """,
        "create": """
            create table if not exists {schema}.Policies (
                policy_id VARCHAR(36),
                user_id VARCHAR(36) NOT NULL,
                quote_id VARCHAR(36) NOT NULL,
                purchase_time DECIMAL NOT NULL,
                policy_type TEXT,
                policy_device TEXT,
                PRIMARY KEY (policy_id)
            );
        """.format(schema=SCHEMA),
        "insert": """
            INSERT INTO {schema}.Policies (policy_id, user_id, quote_id, purchase_time, policy_type, policy_device)
            VALUES (%(policy_id)s::varchar(36), %(user_id)s::varchar(36), %(quote_id)s::varchar(36), %(purchase_time)s::decimal, %(policy_type)s::text, %(policy_device)s::text)
        """.format(schema=SCHEMA),
        "insert_rt": """
            INSERT INTO main.Policies (policy_id, user_id, quote_id, purchase_time, policy_type, policy_device)
            VALUES (?,?,?,?,?,?)
        """,
        "rt_values": ["policy_id", "user_id", "quote_id", "purchase_time", "policy_type", "policy_device"]
    }

    TRANSACTIONS = {
        "name": "Transactions",
        "create": """
            create table if not exists {schema}.Transactions (
                transaction_id VARCHAR(36),
                user_id VARCHAR(36) NOT NULL,
                ref_id VARCHAR(36),
                ref_type text,
                transaction_time DECIMAL NOT NULL,
                successful BOOLEAN,
                card_number TEXT,
                card_expiration_date TEXT,
                card_type TEXT,
                PRIMARY KEY (transaction_id)
            );
        """.format(schema=SCHEMA),
        "create_rt": """
            create table if not exists main.Transactions (
                transaction_id VARCHAR(36),
                user_id VARCHAR(36) NOT NULL,
                ref_id VARCHAR(36),
                ref_type text,
                transaction_time DECIMAL NOT NULL,
                successful BOOLEAN,
                card_number TEXT,
                card_expiration_date TEXT,
                card_type TEXT,
                CONSTRAINT PK_Transactions PRIMARY KEY (transaction_id)
            );
        """,
        "insert": """
            INSERT INTO {schema}.Transactions (transaction_id, user_id, ref_id, ref_type, transaction_time, successful, card_number, card_expiration_date, card_type)
            VALUES (%(transaction_id)s::varchar(36),%(user_id)s::varchar(36),%(ref_id)s::varchar(36), %(ref_type)s::text, %(transaction_time)s::decimal, %(successful)s::boolean, %(card_number)s::text, %(card_expiration_date)s::text, %(card_type)s::text);
        """.format(schema=SCHEMA),
        "insert_rt": """
            INSERT INTO main.Transactions (transaction_id, user_id, ref_id, ref_type, transaction_time, successful, card_number, card_expiration_date, card_type)
            VALUES (?,?,?,?,?,?,?,?,?)
        """,
        "rt_values": ["transaction_id", "user_id", "ref_id", "ref_type", "transaction_time", "successful", "card_number", "card_expiration_date", "card_type"]
    }