from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Theater(models.Model):
    """Theater organization model"""
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extended user profile linked to theater"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Administrator'),
        ('volunteer', 'Volunteer'),
        ('viewer', 'Viewer'),
    ], default='volunteer')
    
    def __str__(self):
        return f"{self.user.username} - {self.theater}"

class Show(models.Model):
    """Main show/production model"""
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='shows')
    title = models.CharField(max_length=200)
    description = models.TextField()
    director = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} - {self.theater.name}"
    
    def total_tickets_sold(self):
        return self.events.aggregate(models.Sum('tickets_sold'))['tickets_sold__sum'] or 0
    
    def total_revenue(self):
        return self.events.aggregate(models.Sum('revenue'))['revenue__sum'] or Decimal('0.00')
    
    def total_capacity(self):
        return self.events.aggregate(models.Sum('capacity'))['capacity__sum'] or 0
    
    def attendance_rate(self):
        capacity = self.total_capacity()
        if capacity > 0:
            return (self.total_tickets_sold() / capacity) * 100
        return 0

class Event(models.Model):
    """Individual performance/event"""
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='events')
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    capacity = models.IntegerField()
    tickets_sold = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return f"{self.show.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"
    
    def attendance_percentage(self):
        if self.capacity > 0:
            return (self.tickets_sold / self.capacity) * 100
        return 0
    
    def tickets_remaining(self):
        return max(0, self.capacity - self.tickets_sold)

class CastMember(models.Model):
    """Cast member for a show"""
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='cast')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='cast_photos/', blank=True, null=True)
    bio = models.TextField(blank=True)
    order = models.IntegerField(default=0)  # For sorting cast list
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} as {self.role}"

class CrewMember(models.Model):
    """Crew/staff member for a show"""
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='crew')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class Ticket(models.Model):
    """Individual ticket sale record"""
    TICKET_TYPES = [
        ('adult', 'Adult'),
        ('student', 'Student'),
        ('senior', 'Senior'),
        ('child', 'Child'),
        ('comp', 'Complimentary'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    purchaser_name = models.CharField(max_length=100, blank=True)
    purchaser_email = models.EmailField(blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.ticket_type} - {self.event}"
    
    def total_price(self):
        return self.price * self.quantity

class AudienceFeedback(models.Model):
    """Audience survey/feedback"""
    RATING_CHOICES = [(i, f"{i} Stars") for i in range(1, 6)]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Feedback for {self.event} - Rating: {self.rating}"

class Report(models.Model):
    """Generated report record"""
    REPORT_TYPES = [
        ('full', 'Full Show Report'),
        ('financial', 'Financial Summary'),
        ('attendance', 'Attendance Report'),
        ('feedback', 'Audience Feedback'),
        ('cast_crew', 'Cast & Crew List'),
    ]
    
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    pdf_file = models.FileField(upload_to='reports/', blank=True, null=True)
    config = models.JSONField(default=dict, blank=True)  # Store report configuration
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.show.title}"

class ImportHistory(models.Model):
    """Track data imports"""
    IMPORT_SOURCES = [
        ('csv', 'CSV Upload'),
        ('excel', 'Excel Upload'),
        ('manual', 'Manual Entry'),
    ]
    
    IMPORT_TYPES = [
        ('tickets', 'Ticket Sales'),
        ('events', 'Events'),
        ('cast', 'Cast Members'),
        ('crew', 'Crew Members'),
        ('feedback', 'Audience Feedback'),
    ]
    
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='imports')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True, blank=True, related_name='imports')
    source = models.CharField(max_length=20, choices=IMPORT_SOURCES)
    import_type = models.CharField(max_length=20, choices=IMPORT_TYPES)
    imported_at = models.DateTimeField(auto_now_add=True)
    imported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    records_imported = models.IntegerField(default=0)
    errors = models.TextField(blank=True)
    file = models.FileField(upload_to='imports/', blank=True, null=True)
    
    class Meta:
        ordering = ['-imported_at']
        verbose_name_plural = 'Import histories'
    
    def __str__(self):
        return f"{self.get_import_type_display()} from {self.get_source_display()} - {self.imported_at.strftime('%Y-%m-%d')}"
