from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

def home(request):
    return HttpResponse("""
        <html>
            <head><title>CS408 Final Project</title></head>
            <body>
                <h1>Hello World!</h1>
                <h2>CS408 Final Project</h2>
                <p>My Django application is running successfully.</p>
            </body>
        </html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
]
