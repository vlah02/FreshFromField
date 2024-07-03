# Nikola Kovacevic 2021/0113
# Djordje Loncar 2021/0076
from django import forms
from django.contrib.auth.hashers import make_password

from .models import *
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    """
    Form for creating and updating a User.

    Attributes:
        type (CharField): User type field.
        password (CharField): Password field with PasswordInput widget.
    """
    type = forms.CharField(max_length=20)
    password_confirmation = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone', 'city', 'country']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', 'Lozinke se ne poklapaju.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.password = make_password(password)
        if commit:
            user.save()
        return user


class ListingForm(forms.ModelForm):
    """
        Form for creating and updating a Listing.

        Attributes:
            image (ImageField): Optional image field.
    """
    class Meta:
        model = Listing
        fields = ['listingname', 'price', 'unit', 'quantity', 'description', 'type', 'image']
        image = forms.ImageField(required=False)


class UserDataForm(forms.ModelForm):
    """
       Form for updating user data.

       Methods:
           clean_username(): Validates the uniqueness of the username.
           clean_email(): Validates the uniqueness of the email.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'city', 'country']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Korisničko ime već postoji.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Email već postoji.')
        return email


class ListingEditForm(forms.ModelForm):
    """
        Form for editing a Listing.

        Attributes:
            TYPE_CHOICES (list): List of choices for the type field.
            UNIT_CHOICES (list): List of choices for the unit field.
            type (ChoiceField): ChoiceField for the type.
            unit (ChoiceField): ChoiceField for the unit.
            description (CharField): CharField with Textarea widget for the description.
            image (ImageField): Optional image field.
    """
    TYPE_CHOICES = [
        ('Voće', 'Voće'),
        ('Povrće', 'Povrće'),
        ('Meso', 'Meso'),
        ('Mlečni proizvodi', 'Mlečni proizvodi'),
        ('Sirovina', 'Sirovina'),
        ('Ostalo', 'Ostalo'),
    ]

    UNIT_CHOICES = [
        ('din/komad', 'din/komad'),
        ('din/kg', 'din/kg'),
        ('din/g', 'din/g'),
        ('din/ml', 'din/ml'),
        ('din/l', 'din/l'),
    ]

    type = forms.ChoiceField(choices=TYPE_CHOICES)
    unit = forms.ChoiceField(choices=UNIT_CHOICES)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)

    class Meta:
        model = Listing
        fields = ['listingname', 'type', 'price', 'unit', 'quantity', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(ListingEditForm, self).__init__(*args, **kwargs)
        self.fields['listingname'].widget.attrs.update(
            {'id': 'naziv', 'name': 'listingname', 'type': 'text', 'required': 'true'})
        self.fields['type'].widget.attrs.update({'id': 'tip', 'name': 'type', 'required': 'true'})
        self.fields['price'].widget.attrs.update({'id': 'cena', 'name': 'price', 'type': 'number', 'required': 'true'})
        self.fields['unit'].widget.attrs.update({'id': 'jedinica', 'name': 'unit', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update(
            {'id': 'kolicina', 'name': 'quantity', 'type': 'number', 'required': 'true'})
        self.fields['description'].widget.attrs.update({'id': 'opis', 'name': 'description', 'required': 'true'})


class MessageForm(forms.ModelForm):
    """
        Form for creating and updating a Message.

        Attributes:
            model (Model): The model associated with this form.
            fields (list): The fields to include in the form.
    """
    class Meta:
        model = Message
        fields = ['text']
