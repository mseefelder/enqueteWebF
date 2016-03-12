from django.contrib import admin

from .models import Question, Choice

admin.site.site_header = "Administrador EnqueteWeb"

admin.site.site_title = "EnqueteWeb"

# Register your models here.

class ChoiceInline(admin.TabularInline):
	model = Choice

class QuestionAdmin(admin.ModelAdmin):
	inlines = [
		ChoiceInline,
	]

admin.site.register(Question, QuestionAdmin)