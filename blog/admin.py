from django.contrib import admin
from .models import Post

#customizing the way models displaying in the admin panel
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')#column names
    list_filter = ('status', 'created', 'publish', 'author')#filter results
    search_fields = ('title', 'body')#searching purpose
    prepopulated_fields = {'slug':('title',)}#slug automatically fill based on title
    raw_id_fields = ('author',)#instead of drop down menu,there is an search option there
    date_hierarchy = 'publish'#below search bar ,there is an option of navigate easly by using date
    ordering = ['status','publish']


admin.site.register(Post,PostAdmin)
