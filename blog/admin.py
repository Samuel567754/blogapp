from django.contrib import admin
from .models import Post, Category, Tag
from django.utils.html import format_html


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'display_categories','author','display_image','display_tags', 'is_published')  # Shows 'is_published' status
    search_fields = ('title', 'content', 'author')  # Search by title and content
    list_filter = ('date_posted', 'categories', 'is_published')  # Filter by date, categories, and publish status
    ordering = ('-date_posted',)  # Order by most recent posts first
    actions = ['mark_as_published', 'mark_as_unpublished']  # Custom actions
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate the slug based on the title
    readonly_fields = ('date_posted',)  # Make the 'date_posted' field read-only
    filter_horizontal = ('categories','tags')  # Adds a horizontal filter widget for many-to-many relations

    # Function to display categories in the list view
    def display_categories(self, obj):
        return ", ".join(category.name for category in obj.categories.all())

    display_categories.short_description = 'Categories'

    # Custom action to mark posts as published
    def mark_as_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} posts marked as published.")

    mark_as_published.short_description = 'Mark selected posts as published'

    # Method to display the image in the admin interface
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "(No image)"
    display_image.short_description = 'Image'


    # Custom action to mark posts as unpublished
    def mark_as_unpublished(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} posts marked as unpublished.")

    mark_as_unpublished.short_description = 'Mark selected posts as unpublished'

    # Method to display tags as comma-separated values
    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    
    display_tags.short_description = 'Tags'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Show category name and description
    search_fields = ('name', 'description')  # Search categories by name and description
    list_filter = ('name',)  # Filter by category name

# Inline for Posts under Categories
class PostInline(admin.TabularInline):
    model = Post.categories.through  # Allows inline editing of posts within categories
    extra = 1  # Number of empty forms to display

class CategoryAdminWithPosts(CategoryAdmin):
    inlines = [PostInline]  # Add the inline to allow editing posts within the category admin


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdminWithPosts)
admin.site.register(Tag)