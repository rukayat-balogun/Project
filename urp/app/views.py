from django.shortcuts import render, redirect
from django.core.paginator import Paginator
   
from .models import Gallery, Event, NewsEvent
from .forms import GalleryForm, EventForm, NewsEventForm



# Homepage view
def index(request):
    recent_news_events = NewsEvent.objects.all()[:1]
    return render(request, 'index.html', {'recent_news_events': recent_news_events})
    

# "Who We Are" view
def who_we_are(request):
    return render(request, 'who-we-are.html')

# "What We Do" view
def what_we_do(request):
    return render(request, 'what-we-do.html')

# Gallery view

def gallery(request):
    images = Gallery.objects.all()
    return render(request, 'gallery.html', {'images': images})

def upload_image(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = GalleryForm()
    return render(request, 'upload_image.html', {'form': form})


# Events view

def events(request):
    events = Event.objects.all()  # Get all events, ordered by newest
    paginator = Paginator(events, 6)  # Show 6 events per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Get events for the current page

    return render(request, 'events.html', {'page_obj': page_obj})


# Contact Us view
def contact_us(request):
    return render(request, 'contact-us.html')

# Partnership view
def partnership(request):
    return render(request, 'partnership.html')
