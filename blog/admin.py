from django.contrib import admin
from django.utils import timezone
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published_date')
    actions = ['make_published']
    search_fields = ['title', 'text', 'author']
    date_hierarchy = 'created_at'

    def make_published(modeladmin, request, queryset):
        queryset.update(published_date=timezone.now())

    make_published.short_description = 'Mark selected posts as published'

    def get_changeform_initial_data(self, request):
        get_data = super(PostAdmin, self).get_changeform_initial_data(request)
        get_data['author'] = request.user.pk
        return get_data


admin.site.register(Post, PostAdmin)