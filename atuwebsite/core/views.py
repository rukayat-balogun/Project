
import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Service, Purchase
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')


def initiate_payment(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not course.is_paid:
        return redirect('course_detail', course_id=course.id)  # Free course, no payment needed

    if not request.user.is_authenticated:
        return redirect('/login/')  # Force login before payment

    amount = int(course.price * 100)  # Paystack accepts amount in Kobo

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "email": request.user.email,  # 👈 Real user's email
        "amount": amount,
        "currency": "NGN",
        "callback_url": request.build_absolute_uri(f'/payment-success/{course.id}/'),
        "metadata": {
            "course_id": course.id,
            "user_id": request.user.id,
        }
    }

    response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
    res_data = response.json()

    if res_data.get('status'):
        auth_url = res_data['data']['authorization_url']
        return redirect(auth_url)
    else:
        return render(request, 'payment_failed.html', {"course": course})



def home(request):
    services = Service.objects.all()
    latest_courses = Course.objects.order_by('-id')[:15]  # Get the last 15 added courses
    return render(request, 'home.html', {'services': services, 'latest_courses': latest_courses})

def search_courses(request):
    query = request.GET.get('q')
    courses = []

    if query:
        courses = Course.objects.filter(course_name__icontains=query)

    return render(request, 'search_results.html', {'courses': courses, 'query': query})


def service_detail(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug)
    courses = service.courses.all()  # Get courses under that service
    return render(request, 'service_detail.html', {'service': service, 'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Option 1: Redirect directly to the file download
    return redirect(course.file.url)


@csrf_exempt
def paystack_webhook(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        event = payload.get('event')

        if event == 'charge.success':
            data = payload['data']
            metadata = data.get('metadata', {})
            course_id = metadata.get('course_id')
            user_id = metadata.get('user_id')
            reference = data['reference']

            try:
                user = User.objects.get(id=user_id)
                course = Course.objects.get(id=course_id)

                # Check if this user already has the purchase
                Purchase.objects.get_or_create(
                    user=user,
                    course=course,
                    payment_reference=reference
                )

            except (User.DoesNotExist, Course.DoesNotExist):
                pass  # In production, you should log this error

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
