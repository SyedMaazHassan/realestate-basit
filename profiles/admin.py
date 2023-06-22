from django.contrib import admin
from .models import TeamMember, SocialProfile, AgentProfile


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')

class AgentProfileAdmin(PersonAdmin):
    list_display = PersonAdmin.list_display + ('name', 'designation')

class TeamMemberAdmin(PersonAdmin):
    list_display = PersonAdmin.list_display + ('designation',)
    list_display += ('created_at',)


class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')


admin.site.register(AgentProfile, AgentProfileAdmin)
admin.site.register(SocialProfile)
admin.site.register(TeamMember, TeamMemberAdmin)
