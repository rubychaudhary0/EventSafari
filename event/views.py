from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def event(request):
    if request.path.startswith('/event/'):
        return redirect('event')
    else:
        return render(request, 'event.html')
    


def create_event(request):
    return render(request, 'events/create_event.html')