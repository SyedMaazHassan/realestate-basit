from django.contrib import admin
from .models import Agent, TeamMember, SocialProfile, AgentProfile


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

class AgentAdmin(PersonAdmin):
    list_display = PersonAdmin.list_display + ('tagline', 'overview')
    list_display += ('created_at',)

class TeamMemberAdmin(PersonAdmin):
    list_display = PersonAdmin.list_display + ('designation',)
    list_display += ('created_at',)


class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')


admin.site.register(AgentProfile, AgentProfileAdmin)
admin.site.register(SocialProfile)
admin.site.register(Agent, AgentAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
