from django import forms
from .models import Theater, Show, Event, CastMember, CrewMember, Ticket, AudienceFeedback
from django.contrib.auth.models import User

class TheaterForm(forms.ModelForm):
    class Meta:
        model = Theater
        fields = ['name', 'address', 'email', 'phone', 'logo']

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['title', 'description', 'director', 'start_date', 'end_date', 'poster']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'venue', 'capacity', 'notes']

class CastMemberForm(forms.ModelForm):
    class Meta:
        model = CastMember
        fields = ['name', 'role', 'email', 'phone', 'photo', 'bio', 'order']

class CrewMemberForm(forms.ModelForm):
    class Meta:
        model = CrewMember
        fields = ['name', 'position', 'email', 'phone', 'order']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'price', 'quantity', 'purchaser_name', 'purchaser_email', 'notes']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = AudienceFeedback
        fields = ['rating', 'comments', 'name', 'email']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV file')
    import_type = forms.ChoiceField(choices=[
        ('events', 'Events'),
        ('cast', 'Cast Members'),
        ('crew', 'Crew Members'),
        ('tickets', 'Ticket Sales'),
        ('feedback', 'Audience Feedback'),
    ])

class ReportConfigForm(forms.Form):
    report_type = forms.ChoiceField(choices=[
        ('full', 'Full Show Report'),
        ('financial', 'Financial Summary'),
        ('attendance', 'Attendance Report'),
        ('feedback', 'Audience Feedback'),
        ('cast_crew', 'Cast & Crew List'),
    ])
    include_charts = forms.BooleanField(required=False, initial=True)
    include_feedback = forms.BooleanField(required=False, initial=True)
    include_cast = forms.BooleanField(required=False, initial=True)
    include_crew = forms.BooleanField(required=False, initial=True)
