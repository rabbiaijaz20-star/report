from django.contrib import admin
from .models import (Theater, UserProfile, Show, Event, CastMember, CrewMember, 
                     Ticket, AudienceFeedback, Report, ImportHistory)

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'theater', 'role']
    list_filter = ['role', 'theater']
    search_fields = ['user__username', 'user__email']

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['title', 'theater', 'director', 'start_date', 'end_date', 'created_by']
    list_filter = ['theater', 'start_date', 'created_at']
    search_fields = ['title', 'director']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['show', 'date', 'venue', 'tickets_sold', 'capacity', 'revenue', 'attendance_percentage']
    list_filter = ['show', 'date', 'venue']
    search_fields = ['show__title', 'venue']
    date_hierarchy = 'date'
    
    def attendance_percentage(self, obj):
        return f"{obj.attendance_percentage():.1f}%"
    attendance_percentage.short_description = 'Attendance %'

@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'show', 'email', 'order']
    list_filter = ['show']
    search_fields = ['name', 'role']
    ordering = ['order', 'name']

@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'show', 'email', 'order']
    list_filter = ['show', 'position']
    search_fields = ['name', 'position']
    ordering = ['order', 'name']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['event', 'ticket_type', 'quantity', 'price', 'total_price', 'purchaser_name', 'purchase_date']
    list_filter = ['ticket_type', 'event__show', 'purchase_date']
    search_fields = ['purchaser_name', 'purchaser_email']
    date_hierarchy = 'purchase_date'
    
    def total_price(self, obj):
        return f"${obj.total_price():.2f}"
    total_price.short_description = 'Total'

@admin.register(AudienceFeedback)
class AudienceFeedbackAdmin(admin.ModelAdmin):
    list_display = ['event', 'rating', 'name', 'submitted_at']
    list_filter = ['rating', 'event__show', 'submitted_at']
    search_fields = ['comments', 'name', 'email']
    date_hierarchy = 'submitted_at'

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['show', 'report_type', 'generated_at', 'generated_by']
    list_filter = ['report_type', 'generated_at', 'show__theater']
    search_fields = ['show__title']
    date_hierarchy = 'generated_at'
    readonly_fields = ['generated_at']

@admin.register(ImportHistory)
class ImportHistoryAdmin(admin.ModelAdmin):
    list_display = ['theater', 'show', 'import_type', 'source', 'records_imported', 'imported_at', 'imported_by']
    list_filter = ['source', 'import_type', 'imported_at', 'theater']
    search_fields = ['show__title', 'theater__name']
    date_hierarchy = 'imported_at'
    readonly_fields = ['imported_at']
