from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .models import Place, PlaceImage, Contact, Review
from django.contrib import messages
from decimal import Decimal
from django.db.models import Avg
from booking.models import Booking


def index_view(request: HttpRequest):
    
    return render(request, "main/index.html")

def about(request: HttpRequest):
    
    return render(request, "main/about.html")

@login_required
def contact_view(request):
    if request.method == 'POST':
        user = request.user  
       
        new_contact = Contact(
            user=user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
       
        new_contact.save()

       
        return redirect('main:contact')  
    else:
        return render(request, 'main/contact_us.html')
    

@login_required
def add_place(request):
    if request.method == 'POST':
        
        user = request.user
        
        name = request.POST.get('name')
        neighborhood = request.POST.get('neighborhood')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        price = request.POST.get('price')
        address = request.POST.get('address')
        category = request.POST.get('category')
        description = request.POST.get('description')
        
        if name and neighborhood and latitude and longitude and price and address and category:
            
            place = Place.objects.create(
                user=user,  
                name=name,
                neighborhood=neighborhood,
                latitude=latitude,
                longitude=longitude,
                price=price,
                address=address,
                category=category,
                description=description,
            )

           
            for i in range(1, 6):  
                image_file = request.FILES.get(f'image{i}')
                if image_file:
                    place_image = PlaceImage(place=place, image=image_file)
                    place_image.save()

            return redirect('main/success_page')
        else:
          
            error_message = 'Please fill in all required fields.'
            return render(request, 'main/add_place.html', {'error_message': error_message})

    return render(request, 'main/add_place.html')

    
    

def success_page_view(request):
    return render(request, 'main/place_added_success.html')

def place_detail(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    average_rating = Review.objects.filter(place=place).aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'place': place,
        'place_id': place_id,
        'average_rating': average_rating,
    }
    
    return render(request, 'main/place_detail.html', context)


def services_page(request):
    return render(request, 'main/services.html')


def all_places_view(request):
    neighborhoods = Place.objects.values_list('neighborhood', flat=True).distinct()
    categories = Place.objects.values_list('category', flat=True).distinct()

    
    neighborhood = request.GET.get('neighborhood')
    category = request.GET.get('category')

   
    filtered_places = Place.objects.all()
    if neighborhood:
        filtered_places = filtered_places.filter(neighborhood=neighborhood)
    if category:
        filtered_places = filtered_places.filter(category=category)

    return render(request, 'main/all_places.html', {'neighborhoods': neighborhoods, 'categories': categories, 'filtered_places': filtered_places})

def ad(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("main:login_view")
    places = Place.objects.filter(user=request.user)
    return render(request, "main/my_ads.html", {'places': places})

def update_place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    
    
    if request.method == 'POST' and request.user.is_staff:
        place.name = request.POST.get('name')
        place.neighborhood = request.POST.get('neighborhood')
        place.latitude = request.POST.get('latitude')
        place.longitude = request.POST.get('longitude')
        place.price = request.POST.get('price')
        place.address = request.POST.get('address')
        place.category = request.POST.get('category')
        place.save()
        
        return redirect('main:place_detail', place_id=place.id)
    
    return render(request, 'main/update_place.html', {'place': place})

def delete_place(request, place_id):
    if not request.user.is_staff:
        return redirect('main:ad')
    
    place = get_object_or_404(Place, pk=place_id)
    place.delete()

    return redirect('main:ad')

@login_required
def add_review(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    user = request.user
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        existing_review = Review.objects.filter(place=place, user=user).first()
        if existing_review:
            return render(request, 'main/review_already_exists.html', {'place': place})
        
        review = Review.objects.create(place=place, rating=rating, comment=comment, user=user)
        return redirect('main:place_detail', place_id=place_id)
    
    return render(request, 'main/add_review.html', {'place': place})


def booking_details(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'main/booking_details.html', {'booking': booking})

@login_required
def all_bookings(request):
    user_places = Place.objects.filter(user=request.user)
    bookings = Booking.objects.filter(place__in=user_places)
    return render(request, 'main/all_bookings.html', {'bookings': bookings})