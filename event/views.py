from django.shortcuts import render, redirect

# Create your views here.
def event(request):
    if request.path.startswith('/event/'):
        return redirect('event')
    else:
        return render(request, 'event.html')
