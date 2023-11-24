from django.contrib import admin
from .models import Specialization, Field, Skill,UserProfile

# Register your models here.
admin.site.register(Specialization)
#admin.site.register(UserProfile)
# admin.site.register(Field)
admin.site.register(Skill)
admin.site.register(UserProfile)
#admin.site.register(UserRecommendations)

class SuperuserOnlyFieldAdmin(admin.ModelAdmin):
    # Customizations for the Field model accessible only by superusers
    list_display = ['field', 'field_name','description']  # Customize as needed
    search_fields = ['field_name']  # Customize as needed
    # ... other customizations

    # def get_model_perms(self, request):
    #     perms = super().get_model_perms(request)
    #     if request.user.is_staff:
       
    #          perms.update({
    #             'view': False,
    #             'add': False,
    #             'change': False,
    #             'delete': False,
    #         })
    #          return perms
    #     return super().has_module_permission(request)

admin.site.register(Field, SuperuserOnlyFieldAdmin)