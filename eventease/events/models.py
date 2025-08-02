from django.db import models
'''class Event(models.Model):
    CATEGORY_CHOICES = [
        ('Concert', 'Concert'),
        ('Picnic', 'Picnic'),
        ('Party', 'Party'),
        ('Workshop', 'Workshop'),
        ('Other', 'Other'),
    ]'''

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('Concert', 'Concert'),
        ('Picnic', 'Picnic'),
        ('Party', 'Party'),
        ('Workshop', 'Workshop'),
        ('Other', 'Other'),
    ]
    title= models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    available_tickets = models.PositiveIntegerField()

    def __str__(self):
        return self.title


