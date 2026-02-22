from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing_app', '0012_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanySettings',
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
                    'nombre_empresa',
                    models.CharField(
                        default='Nombre de la Empresa',
                        max_length=200,
                        verbose_name='Nombre de la Empresa'
                    )
                ),
                (
                    'ruc',
                    models.CharField(
                        blank=True,
                        max_length=20,
                        verbose_name='RUC'
                    )
                ),
                (
                    'direccion_fiscal',
                    models.TextField(
                        blank=True,
                        verbose_name='Dirección Fiscal'
                    )
                ),
                (
                    'logo',
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to='company_logos/',
                        verbose_name='Logo de la Empresa'
                    )
                ),
                (
                    'telefono',
                    models.CharField(
                        blank=True,
                        max_length=50,
                        verbose_name='Teléfono'
                    )
                ),
                (
                    'email',
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        verbose_name='Email'
                    )
                ),
                (
                    'fecha_actualizacion',
                    models.DateTimeField(auto_now=True)
                ),
            ],
            options={
                'verbose_name': 'Configuración de Empresa',
                'verbose_name_plural': 'Configuración de Empresa',
            },
        ),
    ]
