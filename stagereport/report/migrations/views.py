import csv
from io import TextIOWrapper
from decimal import Decimal
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

@login_required
def dashboard(request):
    """Dashboard for logged-in users"""
    profile = request.user.userprofile
    theater = profile.theater
    shows = Show.objects.filter(theater=theater)
    total_revenue = sum(show.total_revenue() for show in shows)
    total_tickets = sum(show.total_tickets_sold() for show in shows)
    total_capacity = sum(show.total_capacity() for show in shows)
    avg_attendance = (total_tickets / total_capacity * 100) if total_capacity > 0 else 0
    context = {
        'theater': theater,
        'shows': shows,
        'total_revenue': total_revenue,
        'total_tickets': total_tickets,
        'avg_attendance': avg_attendance,
    }
    return render(request, 'reports/dashboard.html', context)

@login_required
def show_detail(request, show_id):
    """Detailed view of a show with stats"""
    show = get_object_or_404(Show, id=show_id)
    events = show.events.all()
    cast = show.cast.all()
    crew = show.crew.all()

    total_revenue = show.total_revenue()
    total_tickets = show.total_tickets_sold()
    total_capacity = show.total_capacity()
    avg_attendance = (total_tickets / total_capacity * 100) if total_capacity > 0 else 0
    feedback = AudienceFeedback.objects.filter(event__show=show)
    avg_rating = feedback.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'show': show,
        'events': events,
        'cast': cast,
        'crew': crew,
        'total_revenue': total_revenue,
        'total_tickets': total_tickets,
        'avg_attendance': avg_attendance,
        'avg_rating': avg_rating,
        'feedback': feedback,
    }
    return render(request, 'reports/show_detail.html', context)

@login_required
def setup_theater(request):
    """Initial setup for theater information"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    theater = profile.theater

    if request.method == 'POST':
        form = TheaterForm(request.POST, request.FILES, instance=theater)
        if form.is_valid():
            theater = form.save()
            profile.theater = theater
            profile.save()
            messages.success(request, 'Theater profile saved successfully.')
            return redirect('dashboard')
    else:
        form = TheaterForm(instance=theater)

    return render(request, 'reports/setup_theater.html', {'form': form})

@login_required
def create_show(request):
    """Create a new show"""
    theater = request.user.userprofile.theater
    if request.method == 'POST':
        form = ShowForm(request.POST, request.FILES)
        if form.is_valid():
            show = form.save(commit=False)
            show.theater = theater
            show.created_by = request.user
            show.save()
            messages.success(request, 'Show created successfully.')
            return redirect('show_detail', show_id=show.id)
    else:
        form = ShowForm()
    return render(request, 'reports/create_show.html', {'form': form})

@login_required
def add_event(request, show_id):
    """Add an event/performance to a show"""
    show = get_object_or_404(Show, id=show_id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.show = show
            event.save()
            messages.success(request, 'Event added successfully.')
            return redirect('show_detail', show_id=show.id)
    else:
        form = EventForm()
    return render(request, 'reports/add_event.html', {'form': form, 'show': show})

@login_required
def upload_csv(request, show_id):
    """Handle CSV uploads for import"""
    show = get_object_or_404(Show, id=show_id)
    theater = request.user.userprofile.theater

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            import_type = form.cleaned_data['import_type']
            decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(decoded_file)
            count = 0
            errors = []

            try:
                if import_type == 'events':
                    for row in reader:
                        Event.objects.create(
                            show=show,
                            date=datetime.strptime(row['date'], '%Y-%m-%d %H:%M'),
                            venue=row.get('venue', ''),
                            capacity=int(row.get('capacity', 0)),
                            tickets_sold=int(row.get('tickets_sold', 0)),
                            revenue=Decimal(row.get('revenue', '0.00')),
                            notes=row.get('notes', '')
                        )
                        count += 1
                elif import_type == 'cast':
                    for row in reader:
                        CastMember.objects.create(
                            show=show,
                            name=row['name'],
                            role=row.get('role', ''),
                            email=row.get('email', ''),
                            phone=row.get('phone', ''),
                            order=int(row.get('order', 0))
                        )
                        count += 1
                elif import_type == 'crew':
                    for row in reader:
                        CrewMember.objects.create(
                            show=show,
                            name=row['name'],
                            position=row.get('position', ''),
                            email=row.get('email', ''),
                            phone=row.get('phone', ''),
                            order=int(row.get('order', 0))
                        )
                        count += 1
                elif import_type == 'tickets':
                    for row in reader:
                        event_date = datetime.strptime(row['event_date'], '%Y-%m-%d %H:%M')
                        event = Event.objects.filter(show=show, date=event_date).first()
                        if event:
                            Ticket.objects.create(
                                event=event,
                                ticket_type=row.get('ticket_type', 'adult'),
                                price=Decimal(row.get('price', '0.00')),
                                quantity=int(row.get('quantity', 1)),
                                purchaser_name=row.get('purchaser_name', ''),
                                purchaser_email=row.get('purchaser_email', '')
                            )
                            event.tickets_sold += int(row.get('quantity', 1))
                            event.revenue += Decimal(row.get('price', '0.00')) * int(row.get('quantity', 1))
                            event.save()
                            count += 1
                elif import_type == 'feedback':
                    for row in reader:
                        event_date = datetime.strptime(row['event_date'], '%Y-%m-%d %H:%M')
                        event = Event.objects.filter(show=show, date=event_date).first()
                        if event:
                            AudienceFeedback.objects.create(
                                event=event,
                                rating=int(row.get('rating', 5)),
                                comments=row.get('comments', ''),
                                name=row.get('name', ''),
                                email=row.get('email', '')
                            )
                            count += 1

                ImportHistory.objects.create(
                    theater=theater,
                    show=show,
                    source='csv',
                    import_type=import_type,
                    imported_by=request.user,
                    records_imported=count,
                    errors='\n'.join(errors)
                )
                messages.success(request, f"Imported {count} records successfully.")
                if errors:
                    messages.warning(request, f"{len(errors)} errors occurred during import.")
                return redirect('show_detail', show_id=show.id)
            except Exception as e:
                messages.error(request, f"Import failed: {str(e)}")

    else:
        form = CSVUploadForm()
    return render(request, 'reports/upload_csv.html', {'form': form, 'show': show})

@login_required
def generate_report(request, show_id):
    """Generate report configuration"""
    show = get_object_or_404(Show, id=show_id)
    if request.method == 'POST':
        form = ReportConfigForm(request.POST)
        if form.is_valid():
            Report.objects.create(
                show=show,
                report_type=form.cleaned_data['report_type'],
                generated_by=request.user,
                config=form.cleaned_data
            )
            messages.success(request, 'Report configuration saved successfully.')
            return redirect('show_detail', show_id=show.id)
    else:
        form = ReportConfigForm()
    return render(request, 'reports/generate_report.html', {'form': form, 'show': show})

def submit_feedback(request, event_id):
    """Public audience feedback form"""
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.event = event
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback_thanks')
    else:
        form = FeedbackForm()
    return render(request, 'reports/feedback_form.html', {'form': form, 'event': event})

def feedback_thanks(request):
    """Simple thank-you page after feedback submission"""
    return render(request, 'reports/feedback_thanks.html')
