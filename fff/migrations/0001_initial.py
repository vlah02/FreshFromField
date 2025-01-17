# Generated by Django 4.2.13 on 2024-05-30 23:12

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(db_column='userId', primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=40, unique=True)),
                ('password', models.TextField()),
                ('first_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(max_length=40, unique=True)),
                ('membershipstartdate', models.DateTimeField(db_column='membershipStartDate', default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
                'managed': True,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('chatid', models.AutoField(db_column='chatId', primary_key=True, serialize=False)),
                ('user1', models.ForeignKey(db_column='user1', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'chat',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('listingid', models.AutoField(db_column='listingId', primary_key=True, serialize=False)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('listingname', models.CharField(blank=True, db_column='listingName', max_length=30, null=True)),
                ('unit', models.CharField(blank=True, max_length=30, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('type', models.CharField(blank=True, max_length=30, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.BinaryField(blank=True, editable=True, null=True)),
            ],
            options={
                'db_table': 'listing',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Adminuser',
            fields=[
                ('userid', models.OneToOneField(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'adminuser',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('userid', models.OneToOneField(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'customer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('userid', models.OneToOneField(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('numberOfListings', models.IntegerField(blank=True, db_column='numberOfListings', default=0, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'seller',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('messageid', models.AutoField(db_column='messageId', primary_key=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=500, null=True)),
                ('dateandtime', models.TimeField(blank=True, db_column='dateAndTime', null=True)),
                ('chatid', models.ForeignKey(db_column='chatId', on_delete=django.db.models.deletion.DO_NOTHING, to='fff.chat')),
                ('sender', models.ForeignKey(db_column='sender', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'message',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FavoriteListing',
            fields=[
                ('favid', models.AutoField(db_column='favid', primary_key=True, serialize=False)),
                ('listingid', models.ForeignKey(db_column='listingId', on_delete=django.db.models.deletion.CASCADE, to='fff.listing')),
                ('userid', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.CASCADE, related_name='favorite_listings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorite_listings',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='listing',
            name='userid',
            field=models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, to='fff.seller'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user2',
            field=models.ForeignKey(db_column='user2', on_delete=django.db.models.deletion.DO_NOTHING, to='fff.seller'),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('listingid', models.OneToOneField(db_column='listingId', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='fff.listing')),
                ('userid', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.DO_NOTHING, to='fff.customer')),
            ],
            options={
                'db_table': 'reservation',
                'managed': True,
                'unique_together': {('listingid', 'userid')},
            },
        ),
    ]
