from django.contrib import admin
from main.models import VideoAsset,Course,Wishlist
from import_export.admin import ExportActionMixin
# Register your models here.

class CourseAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ['title','type','price','uploadDate']
    list_filter = ['type']
    search_fields = ['title']
    
    
class VideoAdmin(ExportActionMixin,admin.ModelAdmin):
    fieldsets = (
      ('Video Details', {
          'fields': ('title','tags','course')
      }),
      ('Assets', {
          'fields': ('raw', 'thumbnail')
      }),
   )
    list_display = ['title','uniqueName','uploaded']
    list_filter = ['course']
    search_fields = ['title','tags']
    autocomplete_fields = ["course"]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('course')


admin.site.register(Wishlist)
admin.site.register(Course,CourseAdmin)
admin.site.register(VideoAsset,VideoAdmin)
