from django.db import models

# Create your models here.


class TimeStampModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vendor(TimeStampModel):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_latest_performance(self):
        if not hasattr(self, '_cached_latest_performance'):
            self._cached_latest_performance = HistoricalPerformance.objects.filter(vendor=self).order_by("-created_at").first()

        return self._cached_latest_performance

    @property
    def on_time_delivery_rate(self):
        return self.get_latest_performance().on_time_delivery_rate if self.get_latest_performance() else 0

    @property
    def quality_rating_avg(self):
        return self.get_latest_performance().quality_rating_avg if self.get_latest_performance() else 0

    @property
    def average_response_time(self):
        return self.get_latest_performance().average_response_time if self.get_latest_performance() else 0

    @property
    def fulfillment_rate(self):
        return self.get_latest_performance().fulfillment_rate if self.get_latest_performance() else 0


class PurchaseOrder(TimeStampModel):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"
    STATUS_CHOICES = (
        (PENDING, PENDING),
        (COMPLETED, COMPLETED),
        (CANCELED, CANCELED),
    )

    po_number = models.IntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.po_number:
            # You can set a default value or fetch the max value and increment it
            self.po_number = PurchaseOrder.objects.aggregate(models.Max('po_number'))['po_number__max'] or 0
            self.po_number += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"


class HistoricalPerformance(TimeStampModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date.strftime('%Y-%m-%d')}"


