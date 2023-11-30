from django.contrib import admin
from vms.models import *

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "vendor_code"]


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ["po_number_and_vendor", "status"]

    @admin.display()
    def po_number_and_vendor(self, obj):
        return obj.__str__()


admin.site.register(Vendor, VendorAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(HistoricalPerformance)