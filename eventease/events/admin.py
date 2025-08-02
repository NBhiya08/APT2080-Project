from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'date', 'time','venue', 'price', 'category', 'available_tickets')

admin.site.register(Event)
