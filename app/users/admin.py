from django.contrib import admin
from .models import User, Skill


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'surname', 'email', 'role', 'display_skills')
    search_fields = ('username', 'first_name', 'last_name', 'surname', 'email', 'role', 'display_skills')

    def display_skills(self, obj):
        """Returns user skills."""
        return ", ".join([skill.name for skill in obj.skills.all()])

    display_skills.short_description = 'Навыки'


admin.site.register(Skill)
