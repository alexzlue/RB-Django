from django.contrib import admin

from .models import Choice, Question, Company


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    exclude = ['pub_date']
    readonly_fields = ('question_text',)
    extra = 0
    max_num = 0


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Company', {'fields': ['company']})
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_display = ('question_text', 'pub_date', 'was_published_recently')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    ordering = ('name',)
    inlines = [QuestionInline]

admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Company, CompanyAdmin)
