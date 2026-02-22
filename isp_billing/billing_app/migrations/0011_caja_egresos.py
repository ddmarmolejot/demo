from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing_app', '0010_add_ot_exonerada'),
    ]

    operations = [
        migrations.CreateModel(
            name='EgresoConcepto',
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
                ('nombre', models.CharField(max_length=120, unique=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Egreso',
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
                ('fecha', models.DateField()),
                (
                    'tipo_comprobante',
                    models.CharField(
                        choices=[
                            ('RECIBO', 'Recibo'),
                            ('BOLETA', 'Boleta'),
                            ('FACTURA', 'Factura'),
                            ('OTRO', 'Otro')
                        ],
                        default='RECIBO',
                        max_length=20
                    )
                ),
                (
                    'numero_comprobante',
                    models.CharField(blank=True, max_length=30)
                ),
                (
                    'monto',
                    models.DecimalField(decimal_places=2, max_digits=10)
                ),
                ('responsable', models.CharField(max_length=120)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'concepto',
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name='egresos',
                        to='billing_app.egresoconcepto'
                    )
                ),
            ],
        ),
    ]
