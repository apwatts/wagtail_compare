from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubsitePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=models.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
