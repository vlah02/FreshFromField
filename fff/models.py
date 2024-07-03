# Nikola Kovacevic 2021/0113
# Djordje Loncar 2021/0076


from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class Adminuser(models.Model):
    """
        Adminuser model that extends User model with one-to-one relationship.

        Attributes:
            userid (OneToOneField): One-to-one relationship with User model.
    """
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId',
                                  primary_key=True)

    class Meta:
        managed = True
        db_table = 'adminuser'


class Chat(models.Model):
    """
        Chat model representing a chat between two users.

        Attributes:
            chatid (AutoField): Primary key for chat ID.
            user2 (ForeignKey): Foreign key to Seller model.
            user1 (ForeignKey): Foreign key to User model.
    """
    chatid = models.AutoField(db_column='chatId', primary_key=True)
    user2 = models.ForeignKey('Seller', models.DO_NOTHING, db_column='user2')
    user1 = models.ForeignKey('User', models.DO_NOTHING, db_column='user1')

    class Meta:
        managed = True
        db_table = 'chat'


class Customer(models.Model):
    """
        Customer model that extends User model with one-to-one relationship.

        Attributes:
            userid (OneToOneField): One-to-one relationship with User model.
            rating (DecimalField): Customer rating.
    """
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId',
                                  primary_key=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'customer'


class Listing(models.Model):
    """
        Listing model representing an item listed by a seller.

        Attributes:
            listingid (AutoField): Primary key for listing ID.
            price (IntegerField): Price of the listing.
            listingname (CharField): Name of the listing.
            unit (CharField): Unit of the listing.
            quantity (IntegerField): Quantity available.
            description (CharField): Description of the listing.
            type (CharField): Type of the listing.
            date_added (DateTimeField): Date the listing was added.
            image (BinaryField): Image of the listing.
            userid (ForeignKey): Foreign key to Seller model.
    """
    listingid = models.AutoField(db_column='listingId', primary_key=True)
    price = models.IntegerField(blank=True, null=True)
    listingname = models.CharField(db_column='listingName', max_length=30, blank=True,
                                   null=True)
    unit = models.CharField(max_length=30, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    image = models.BinaryField(null=True, blank=True, editable=True)
    userid = models.ForeignKey('Seller', models.DO_NOTHING, db_column='userId')

    class Meta:
        managed = True
        db_table = 'listing'


class Message(models.Model):
    """
        Message model representing a message in a chat.

        Attributes:
            messageid (AutoField): Primary key for message ID.
            text (CharField): Text content of the message.
            dateandtime (TimeField): Date and time of the message.
            chatid (ForeignKey): Foreign key to Chat model.
            sender (ForeignKey): Foreign key to User model (sender).
    """
    messageid = models.AutoField(db_column='messageId', primary_key=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    dateandtime = models.TimeField(db_column='dateAndTime', blank=True, null=True)
    chatid = models.ForeignKey(Chat, models.DO_NOTHING, db_column='chatId')
    sender = models.ForeignKey('User', models.DO_NOTHING, db_column='sender')

    class Meta:
        managed = True
        db_table = 'message'


class Reservation(models.Model):
    """
        Reservation model representing a reservation of a listing by a customer.

        Attributes:
            listingid (OneToOneField): One-to-one relationship with Listing model.
            userid (ForeignKey): Foreign key to Customer model.
    """
    listingid = models.OneToOneField(Listing, models.DO_NOTHING, db_column='listingId', primary_key=True)
    userid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='userId')

    class Meta:
        managed = True
        db_table = 'reservation'
        unique_together = (('listingid', 'userid'),)


class Seller(models.Model):
    """
        Seller model that extends User model with one-to-one relationship.

        Attributes:
            userid (OneToOneField): One-to-one relationship with User model.
            numberOfListings (IntegerField): Number of listings the seller has.
            rating (DecimalField): Seller rating.
    """
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId',
                                  primary_key=True)
    numberOfListings = models.IntegerField(db_column='numberOfListings', blank=True, null=True,
                                           default=0)
    rating = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)

    class Meta:
        managed = True
        db_table = 'seller'


from django.utils import timezone


class User(AbstractUser):
    """
        User model that extends Django's AbstractUser.

        Attributes:
            userid (AutoField): Primary key for user ID.
            username (CharField): Unique username.
            password (TextField): Password field.
            first_name (CharField): First name of the user.
            last_name (CharField): Last name of the user.
            phone (CharField): Phone number of the user.
            city (CharField): City of the user.
            country (CharField): Country of the user.
            email (CharField): Unique email address.
            membershipstartdate (DateTimeField): Membership start date.
            last_login (DateTimeField): Last login date and time.
            is_superuser (BooleanField): Boolean indicating if the user is a superuser.
            is_staff (BooleanField): Boolean indicating if the user is a staff member.
            is_active (BooleanField): Boolean indicating if the user account is active.
            date_joined (DateTimeField): Date and time when the user joined.
    """
    userid = models.AutoField(db_column='userId', primary_key=True)
    username = models.CharField(unique=True, max_length=40)
    password = models.TextField()
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=40)
    membershipstartdate = models.DateTimeField(db_column='membershipStartDate',
                                               default=timezone.now)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    last_login = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'user'


class FavoriteListing(models.Model):
    """
        FavoriteListing model representing a user's favorite listing.

        Attributes:
            favid (AutoField): Primary key for favorite listing ID.
            listingid (ForeignKey): Foreign key to Listing model.
            userid (ForeignKey): Foreign key to User model with related name for reverse relation.
    """
    favid = models.AutoField(db_column='favid', primary_key=True)
    listingid = models.ForeignKey(Listing, models.CASCADE, db_column='listingId')
    userid = models.ForeignKey(User, models.CASCADE, db_column='userId', related_name='favorite_listings')

    class Meta:
        managed = True
        db_table = 'favorite_listings'


class Rating(models.Model):
    ratingid = models.AutoField(db_column='ratingId', primary_key=True)  # Field name made lowercase.
    user1 = models.ForeignKey('User', models.DO_NOTHING, db_column='user1')
    user2 = models.ForeignKey('User', models.DO_NOTHING, db_column='user2', related_name='rating_user2_set'
                              )
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        managed = True
        db_table = 'rating'
