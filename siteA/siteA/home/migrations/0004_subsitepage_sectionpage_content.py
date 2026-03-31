from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0001_squashed_0021"),
        ("home", "0003_subsitepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="subsitepage",
            name="hero_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
            ),
        ),
        migrations.AddField(
            model_name="subsitepage",
            name="intro",
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name="SectionPage",
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
                ("nav_label", models.CharField(blank=True, max_length=80)),
                ("intro", models.TextField(blank=True)),
                ("body", wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
