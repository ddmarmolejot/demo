from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing_app', '0009_movimientos_deuda_libres'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordentecnica',
            name='exonerada',
            field=models.BooleanField(default=False),
        ),
    ]
