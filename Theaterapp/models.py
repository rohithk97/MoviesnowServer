from django.db import models
from userapp.models import User
from filmapp.models import Movie 
import uuid
from django.db.models import JSONField

class Theater(models.Model):
    name = models.CharField(max_length=100)
    licence = models.FileField(max_length=50, upload_to='theater_licences/', blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to='theater_photos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    owner=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_active = models.BooleanField(default=True) 
    blocked = models.BooleanField(default=False)
    movies = models.ManyToManyField(Movie, related_name='theaters', blank=True)

    def __str__(self):
        return self.name
    

class Seat(models.Model):
    seat_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    row_number = models.IntegerField()
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.row_number}-{self.seat_number} in {self.theater.name}"
    
    
        
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    seats_booked = JSONField()
    date = models.DateField() 
    time = models.TimeField()
    status = models.CharField(max_length=20, default='Booked')
    def __str__(self):
        return f"Booking for {self.movie.title} at {self.theater.name} by {self.user.name}"     
    
    
    

class TimeSlot(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='time_slot_movies')
    slot_time = models.TimeField()  # Field for the time of the time slot
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='time_slots')

    def __str__(self):
        return f"{self.movie.title} - {self.slot_time}"
    
    

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_id=models.CharField(max_length=100, unique=True)
    
    bookings=models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return f'Payment: {self.amount} (Method: {self.method})'    