from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing_app', '0011_caja_egresos'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppRole',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('can_cobrar', models.BooleanField(default=False)),
                ('can_delete_cliente', models.BooleanField(default=False)),
                ('can_view_deuda', models.BooleanField(default=True)),
                ('can_manage_ots', models.BooleanField(default=True)),
                ('can_manage_ajustes', models.BooleanField(default=False)),
                ('can_manage_caja', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'role',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='users',
                        to='billing_app.approle'
                    )
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
        ),
    ]
