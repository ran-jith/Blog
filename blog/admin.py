from django.contrib import admin
from .models import Post, Comment

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


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')
admin.site.register(Comment,CommentAdmin)
