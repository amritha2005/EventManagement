from django.db import models
from django.contrib.auth.models import User

class CategoryDb(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.category_name
class EventDb(models.Model):

    event_name = models.CharField(max_length=200)
    description = models.TextField()

    category = models.ForeignKey(
        CategoryDb,
        on_delete=models.CASCADE,
        related_name='events'
    )

    event_date = models.DateField()
    event_time = models.TimeField()

    venue = models.CharField(max_length=200)

    ticket_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_events'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name
class BookingDb(models.Model):

    BOOKING_STATUS = (
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
    )

    event = models.ForeignKey(
        EventDb,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    number_of_tickets = models.PositiveIntegerField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    booking_status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default='Booked'
    )

    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_by.username} - {self.event.event_name}"