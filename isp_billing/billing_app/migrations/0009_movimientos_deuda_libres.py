from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing_app', '0008_add_ot_plan_servicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(max_length=50)),
                ('detalle', models.TextField()),
                ('icono', models.CharField(default='fa-info-circle', max_length=50)),
                ('clase', models.CharField(default='secondary', max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientos_historial', to='billing_app.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='DeudaExcluida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo_mes', models.DateField(blank=True, null=True)),
                ('motivo', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deudas_excluidas', to='billing_app.cliente')),
                ('ot_asociada', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing_app.ordentecnica')),
                ('plan_asociado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing_app.clienteplan')),
            ],
            options={},
        ),
        migrations.CreateModel(
            name='SerieCorrelativoLibre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('serie_correlativo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='libres', to='billing_app.seriecorrelativo')),
            ],
            options={},
        ),
        migrations.AddConstraint(
            model_name='deudaexcluida',
            constraint=models.UniqueConstraint(fields=('cliente', 'plan_asociado', 'periodo_mes'), name='uniq_deuda_excluida_plan_periodo'),
        ),
        migrations.AddConstraint(
            model_name='deudaexcluida',
            constraint=models.UniqueConstraint(fields=('cliente', 'ot_asociada'), name='uniq_deuda_excluida_ot'),
        ),
        migrations.AlterUniqueTogether(
            name='seriecorrelativolibre',
            unique_together={('serie_correlativo', 'numero')},
        ),
    ]
