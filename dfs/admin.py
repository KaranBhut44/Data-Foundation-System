from django.contrib import admin
from .models import Dataset_info,Approved_req,Pending_req,Rejected_req
# Register your models here.

admin.site.register(Dataset_info)
admin.site.register(Approved_req)
admin.site.register(Pending_req)
admin.site.register(Rejected_req)


