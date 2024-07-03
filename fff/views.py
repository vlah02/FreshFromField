# Maksim Mihailovic 2021/0092
# Nikola Kovacevic 2021/0113
# Djordje Loncar 2021/0076
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.http import HttpResponse, JsonResponse
from .forms import UserForm, ListingForm, UserDataForm, ListingEditForm, MessageForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.shortcuts import render
from django.http import JsonResponse
from .models import FavoriteListing
from django.db.models import Q, F
import json
from django.db.models import Sum
from django.db.models import Count


def home(request):
    """
        Renders the home page.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The rendered home page.
        """
    return render(request, 'fff/home.html')


def profile(request, pk):
    chat = get_object_or_404(Chat, chatid=pk)
    user_id = chat.user2.userid.userid
    if user_id == request.user.userid:
        user_id = chat.user1.userid

    user = get_object_or_404(User, userid=user_id)

    try:
        usersc = Seller.objects.get(userid=user.userid)
    except:
        usersc = Customer.objects.get(userid=user.userid)
    return render(request, 'fff/profile.html', {'user': user, 'rating': usersc.rating})


def rate(request, pk):
    user2 = get_object_or_404(User, userid=pk)
    rate = request.POST.get('rating')
    #print(rate)
    user1 = request.user
    result = Rating.objects.filter(user1=user1, user2=user2)

    if result.exists():
        rating = Rating.objects.get(user1=user1, user2=user2)
        rating.rating = rate
        rating.save()
    else:
        rating = Rating.objects.create(user1=user1, user2=user2, rating=rate)

    sum = Rating.objects.filter(user2=user2).aggregate(total_rating=Sum('rating'))['total_rating']
    num = Rating.objects.filter(user2=user2).aggregate(total_count=Count('rating'))['total_count']

    try:
        user = Seller.objects.get(userid=user2.userid)
    except:
        user = Customer.objects.get(userid=user2.userid)

    user.rating = sum / num

    user.save()

    return redirect('chats')


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import UserForm
from .models import Seller, Customer

def register(request):
    form_errors = {}
    if request.method == 'POST':
        form = UserForm(request.POST)

        # Manual validation
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        account_type = request.POST.get('type')
        city = request.POST.get('city')
        username = request.POST.get('username')
        country = request.POST.get('country')

        if not first_name:
            form_errors['first_name'] = 'Ime je obavezno.'
        if not last_name:
            form_errors['last_name'] = 'Prezime je obavezno.'
        if not email:
            form_errors['email'] = 'Email je obavezan.'
        if not phone:
            form_errors['phone'] = 'Broj telefona je obavezan.'
        if not password:
            form_errors['password'] = 'Lozinka je obavezna.'
        if password != password_confirmation:
            form_errors['password_confirmation'] = 'Lozinke se ne poklapaju.'
        if not account_type:
            form_errors['type'] = 'Tip naloga je obavezan.'
        if not city:
            form_errors['city'] = 'Grad je obavezan.'
        if not username:
            form_errors['username'] = 'Username je obavezan.'
        if not country:
            form_errors['country'] = 'Drzava je obavezna.'
        if User.objects.filter(username=username).exists():
            form_errors['username'] = 'Username već postoji.'
        if User.objects.filter(email=email).exists():
            form_errors['email'] = 'Email već postoji.'

        if form.is_valid() and not form_errors:
            user_type = form.cleaned_data['type']
            del form.cleaned_data['type']
            user = form.save()

            if user_type == 'seller':
                seller = Seller.objects.create(userid=user)
                seller.save()
            elif user_type == 'customer':
                customer = Customer.objects.create(userid=user)
                customer.save()
            return redirect('home')

    else:
        form = UserForm()

    return render(request, 'fff/registar.html', {'form': form, 'form_errors': form_errors})



def authenticate(request, email=None, password=None):
    """
       Authenticates a user by email and password.

       Args:
           request (HttpRequest): The request object.
           email (str): The user's email.
           password (str): The user's password.

       Returns:
           User: The authenticated user or None if authentication fails.
    """
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):  # ovo radi zamo za usere koji imaju password sacuvan u bazi kao hash
            return user

    except User.DoesNotExist:
        return None


def user_login(request):
    """
        Handles user login.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The login page or redirect to home page upon successful login.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        email_error = None
        password_error = None

        # Check if the email exists in the database
        if not User.objects.filter(email=email).exists():
            email_error = 'Email ne postoji.'
        else:
            user = authenticate(request, email=email, password=password)
            if user is None:
                password_error = 'Uneli ste pogrešnu šifru.'

        if email_error or password_error:
            return render(request, 'fff/login.html', {
                'email_error': email_error,
                'password_error': password_error,
                'email': email,
                'password': password
            })

        # If the email and password are correct
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            request.session['logged_in'] = True

            try:
                seller = Seller.objects.get(userid=user)
                request.session['type'] = 'seller'
            except Seller.DoesNotExist:
                request.session['type'] = 'customer'

            return redirect('home')
        else:
            messages.error(request, 'Pogrešno uneti mail ili šifra.')
            return render(request, 'fff/login.html')

    return render(request, 'fff/login.html')


def logout_view(request):
    """
        Handles user logout.

        Args:
            request (HttpRequest): The request object.

        Returns:
            JsonResponse: A JSON response indicating logout success or failure.
    """
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def new_listing(request):
    """
        Handles the creation of a new listing.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The new listing page or redirect to home page upon successful creation.
    """
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            # Get the Seller instance associated with the current user
            seller_instance = Seller.objects.get(userid=request.user)
            Seller.objects.filter(userid=request.user).update(numberOfListings=F('numberOfListings') + 1)
            # Assign the Seller instance to the userid field
            new_listing = form.save(commit=False)
            new_listing.userid = seller_instance
            # Save the form without committing to the database yet
            new_listing.save()
            # Handle image separately
            if 'image' in request.FILES:
                new_listing.image = request.FILES['image'].read()
                new_listing.save()
            return redirect('/')
        else:
            form = ListingForm()
            return render(request, 'fff/newlisting.html', {'form': form})


    else:
        form = ListingForm()

    return render(request, 'fff/newlisting.html', {'form': form})


def editListing(request, pk):
    """
        Handles the editing of a listing.

        Args:
            request (HttpRequest): The request object.
            pk (int): The primary key of the listing to edit.

        Returns:
            HttpResponse: The edit listing page or redirect to home page upon successful edit.
    """
    listing = get_object_or_404(Listing, listingid=pk)
    if request.method == 'POST':
        form = ListingEditForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            image_file = request.FILES.get('image')
            if image_file:
                listing.image = image_file.read()  # Read and save binary data
            form.save()
            return redirect('home')  # Ensure 'home' URL name is correct
    else:
        form = ListingEditForm(instance=listing)
    return render(request, 'fff/editListing.html', {'form': form})


def deleteListing(request, pk):
    """
        Handles the deletion of a listing.

        Args:
            request (HttpRequest): The request object.
            pk (int): The primary key of the listing to delete.

        Returns:
            HttpResponse: The delete listing page or redirect to home page upon successful deletion.
    """
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        listing.delete()
        return redirect('home')  # Ensure 'home' URL name is correct
    return render(request, 'fff/deleteListing.html', {'listing': listing})


def listing(request, pk):
    """
        Renders the details of a listing.

        Args:
            request (HttpRequest): The request object.
            pk (int): The primary key of the listing.

        Returns:
            HttpResponse: The listing detail page.
    """
    user_favorite_listings = {}
    listing = get_object_or_404(Listing, pk=pk)

    if request.user.is_authenticated:
        user = request.user
        user_favorite_listings = FavoriteListing.objects.filter(userid=user).values_list('listingid', flat=True)
    return render(request, 'fff/listing.html', {'listing': listing, 'user_favorite_listings': user_favorite_listings})


def listings(request):
    """
        Renders a list of listings based on user or category.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The listings page.
    """
    category = request.GET.get('category')
    if category:
        listings = Listing.objects.filter(type=category)
        request.session['category'] = category
    else:
        listings = Listing.objects.filter(userid=request.user.pk)
        request.session['category'] = "nista"
    return render(request, 'fff/listings.html', {'listings': listings})


def favorites(request):
    """
        Handles adding and removing listings from favorites.

        Args:
            request (HttpRequest): The request object.

        Returns:
            JsonResponse: A JSON response indicating if the listing is a favorite.
            HttpResponse: The favorites page.
    """
    is_favorite = False  # Default value for is_favorite

    if request.method == 'POST' and request.user.is_authenticated:
        listing_id = request.POST.get('listing_id')
        user = request.user

        try:
            # Check if the favorite listing already exists for the user
            favorite_listing = FavoriteListing.objects.get(listingid_id=listing_id, userid=user)
            # If it exists, remove it
            favorite_listing.delete()
            is_favorite = False
        except FavoriteListing.DoesNotExist:
            # If it doesn't exist, create it
            listing = Listing.objects.get(pk=listing_id)  # Retrieve the Listing instance
            FavoriteListing.objects.create(listingid=listing, userid=user)
            is_favorite = True

        # Return the JSON response with the is_favorite variable
        return JsonResponse({'is_favorite': is_favorite})
    elif request.user.is_authenticated:
        # Retrieve the user's favorite listings
        favorite_listings = FavoriteListing.objects.filter(userid=request.user)
        # Pass the favorite_listings and is_favorite to the template context
        return render(request, 'fff/favorites.html',
                      {'favorite_listings': favorite_listings, 'is_favorite': is_favorite})
    else:
        # If the user is not authenticated, redirect to the login page
        messages.error(request, 'Morate se ulogovati prvo!')
        return redirect('login')


def update_data(request):
    """
        Handles updating user data.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The user data page or redirect to home page upon successful update.
    """
    if request.method == 'POST':
        form = UserDataForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserDataForm(instance=request.user)

    return render(request, 'fff/userData.html', {'form': form})


def get_chat(request):
    """
        Retrieves or creates a chat between two users.

        Args:
            request (HttpRequest): The request object.

        Returns:
            JsonResponse: A JSON response with the chat ID or an error message.
    """

    if request.method == 'POST':
        user2 = request.POST.get('user2')
        user2 = get_object_or_404(Seller, userid=user2)
        user1 = get_object_or_404(User, userid=request.user.userid)
        chat = Chat.objects.filter(user1=user1, user2=user2).first()
        if chat is None:
            chat = Chat.objects.create(user1=user1, user2=user2)
        return JsonResponse({'chat_id': chat.chatid})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def get_chat_admin(request):
    """
        Retrieves or creates a chat between an admin and a user.

        Args:
            request (HttpRequest): The request object.

        Returns:
            JsonResponse: A JSON response with the chat ID or an error message.
    """
    if request.method == 'POST':
        admin = request.POST.get('user2')
        user2 = get_object_or_404(Seller, userid=admin)
        user1 = get_object_or_404(User, userid=request.user.userid)
        chat = Chat.objects.filter(user1=user1, user2=user2).first()
        if chat is None:
            chat = Chat.objects.create(user1=user1, user2=user2)
        return JsonResponse({'chat_id': chat.chatid})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def chats(request):
    """
        Renders the chat overview page.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The chats overview page.
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Morate se ulogovati prvo!')
        return redirect('login')
    current_user_id = request.user.userid
    chats = Chat.objects.filter(Q(user1=current_user_id) | Q(user2=current_user_id))
    chats_with_users = []

    for chat in chats:
        other_user_id = chat.user2.userid.userid if chat.user1.userid == current_user_id else chat.user1.userid
        other_user = User.objects.get(userid=other_user_id)

        chats_with_users.append({'chat': chat, 'other_user': other_user})

    return render(request, 'fff/chats.html', {'chats': chats_with_users})


def chat(request, chat_id):
    """
        Renders the chat detail page.

        Args:
            request (HttpRequest): The request object.
            chat_id (int): The chat ID.

        Returns:
            HttpResponse: The chat detail page.
    """
    chat = get_object_or_404(Chat, chatid=chat_id)
    messages = Message.objects.filter(chatid=chat_id)
    return render(request, 'fff/chat.html', {'messages': messages, 'chat_id': chat_id})


def create_message(request, chat_id):
    """
       Handles the creation of a new message in a chat.

       Args:
           request (HttpRequest): The request object.
           chat_id (int): The chat ID.

       Returns:
           HttpResponse: The chat detail page.
    """
    print("Create message")
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.dateandtime = timezone.now()
            message.chatid = Chat.objects.get(chatid=chat_id)
            message.sender = request.user
            message.save()
            return redirect('chat', chat_id=chat_id)
    else:
        form = MessageForm()

    return render(request, 'fff/chat.html')


from django.db.models import Q


def search_listinngs(request):
    """
        Searches for listings based on a query.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The search results page.
    """
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query)
    user_ids = [user.userid for user in users]

    listings = Listing.objects.filter(Q(listingname__icontains=query)
                                      | Q(description__icontains=query)
                                      | Q(userid__in=user_ids)).distinct()
    # for l in listings:
    #     print(l.listingname)

    return render(request, 'fff/search.html', {'listings': listings})
