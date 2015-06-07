from django.core.management.color import no_style
from django.db import connection


def detect_type(value):
    if type(value) == str:
        value = value.lower()
        if value == 'true':
            return True
        elif value == 'false':
            return False
        elif value == 'none':
            return None

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

    return value


def sync_models(model_list):
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)
    created_models = set()
    pending_references = {}
    cursor = connection.cursor()

    for model in model_list:
        sql, references = connection.creation.sql_create_model(
            model, no_style(), seen_models)
        seen_models.add(model)
        created_models.add(model)

        for refto, refs in references.items():
            pending_references.setdefault(refto, []).extend(refs)
            if refto in seen_models:
                sql.extend(connection.creation.sql_for_pending_references(
                    refto, no_style(), pending_references))
        sql.extend(connection.creation.sql_for_pending_references(
            model, no_style(), pending_references))

        for statement in sql:
            cursor.execute(statement)

        tables.append(connection.introspection.table_name_converter(
            model._meta.db_table))
