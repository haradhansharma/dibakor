from django.contrib import admin
from .models import *




admin.site.register(ParsedData)

admin.site.register(SlideShow)
admin.site.register(Blocks)
admin.site.register(ExSite)

@admin.register(Parser)
class ParserAdmin(admin.ModelAdmin):
    list_display = ('feed_name','category','parser_type',)
    prepopulated_fields = {'slug': ('feed_name',)}
    
@admin.register(ParserCategory)
class ParserCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','department',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}  



def send_newsletter(modeladmin, request, queryset):
    for newsletter in queryset:
        newsletter.send(request)
send_newsletter.short_description = "Send selected Newsletters to all subscribers"

class NewsletterAdmin(admin.ModelAdmin):
    actions = [send_newsletter]
        
        
admin.site.register(Subscriber)
admin.site.register(Newsletter, NewsletterAdmin)

@admin.register(Informaion)
class InformaionAdmin(admin.ModelAdmin):
    list_display = ('name','content')
    prepopulated_fields = {'slug': ('name',)}
    

     





