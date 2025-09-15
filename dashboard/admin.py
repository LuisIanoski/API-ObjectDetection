from django.contrib import admin
from .models import Dashboard

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('dashboard_id', 'name', 'created_at')
    search_fields = ('dashboard_id', 'name')
    filter_horizontal = ('cameras',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('dashboard_id', 'created_at')
        return ('created_at',)
