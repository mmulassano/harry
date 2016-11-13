from django.contrib import admin



# Register your models here.
from .models import Threat,TypeThreat,Detection


# Register your models here.
admin.site.register(TypeThreat)
admin.site.register(Threat)
admin.site.register(Detection)
