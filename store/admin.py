from django.contrib import admin
from .models import CableList, CablePlan, DataPlan, Disco, NetworkList


admin.site.register(NetworkList)
admin.site.register(DataPlan)
admin.site.register(CableList)
admin.site.register(CablePlan)
admin.site.register(Disco)
