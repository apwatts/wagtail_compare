from django.db import migrations


def repair_wagtailcore_revision(apps, schema_editor):
    connection = schema_editor.connection
    table_name = "wagtailcore_revision"
    column_name = "submitted_for_moderation"
    index_name = "wagtailcore_revision_submitted_for_moderation_9d7e7f7_idx"

    with connection.cursor() as cursor:
        columns = [
            column.name
            for column in connection.introspection.get_table_description(cursor, table_name)
        ]
        if column_name not in columns:
            cursor.execute(
                f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" bool NOT NULL DEFAULT 0'
            )

        constraints = connection.introspection.get_constraints(cursor, table_name)
        if index_name not in constraints:
            cursor.execute(
                f'CREATE INDEX "{index_name}" ON "{table_name}" ("{column_name}")'
            )


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0016_alter_homepage_body"),
    ]

    operations = [
        migrations.RunPython(repair_wagtailcore_revision, migrations.RunPython.noop),
    ]
