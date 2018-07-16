# Generated by Django 2.0.6 on 2018-07-10 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0005_remove_product_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('idcustomer', models.AutoField(db_column='idCustomer', primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=45)),
                ('lastname', models.CharField(max_length=45)),
                ('address', models.TextField()),
                ('tel', models.CharField(max_length=45)),
                ('username', models.CharField(blank=True, max_length=45, null=True)),
                ('password', models.CharField(blank=True, max_length=45, null=True)),
                ('create', models.DateTimeField()),
            ],
            options={
                'db_table': 'customer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('iddocument', models.AutoField(db_column='idDocument', primary_key=True, serialize=False)),
                ('no_field', models.CharField(db_column='No.', max_length=45, unique=True)),
                ('create', models.DateTimeField()),
            ],
            options={
                'db_table': 'document',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('idgoods', models.AutoField(db_column='idGoods', primary_key=True, serialize=False)),
                ('sn', models.CharField(db_column='SN', max_length=45, unique=True)),
                ('detail', models.TextField(db_column='Detail')),
            ],
            options={
                'db_table': 'goods',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('idstaff', models.AutoField(db_column='idStaff', primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=45)),
                ('lastname', models.CharField(max_length=45)),
                ('address', models.TextField()),
                ('tel', models.CharField(max_length=45)),
                ('username', models.CharField(max_length=45, unique=True)),
                ('password', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'staff',
                'managed': False,
            },
        ),
    ]
