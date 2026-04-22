from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PriceHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("symbol", models.CharField(db_index=True, max_length=32)),
                ("price", models.FloatField()),
                ("created_at_utc", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
            ],
            options={"ordering": ["-id"]},
        ),
    ]
