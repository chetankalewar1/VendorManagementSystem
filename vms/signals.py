from django.db.models.signals import post_save
from django.dispatch import receiver
from vms.models import PurchaseOrder, HistoricalPerformance
from django.db import models
from django.db.models import Avg


def calc_on_time_delivery_rate(po):
    # On-Time Delivery Rate
    completed_pos = PurchaseOrder.objects.filter(vendor=po.vendor, status='completed')
    on_time_deliveries = completed_pos.filter(delivery_date__lte=models.F('acknowledgment_date'))
    on_time_delivery_rate = on_time_deliveries.count() / completed_pos.count() * 100 if completed_pos.count() > 0 else 0

    # Quality Rating Average
    quality_ratings = completed_pos.exclude(quality_rating__isnull=True).aggregate(
        average_quality_rating=Avg('quality_rating'))
    quality_rating_avg = quality_ratings['average_quality_rating'] if quality_ratings[
        'average_quality_rating'] else 0

    # Average Response Time (in days)
    response_times = completed_pos.exclude(acknowledgment_date__isnull=True).aggregate(
        average_response_time=Avg(models.F('acknowledgment_date') - models.F('issue_date')))
    average_response_time = response_times['average_response_time'].days if response_times[
        'average_response_time'] else 0

    # Fulfilment Rate
    total_pos = PurchaseOrder.objects.filter(vendor=po.vendor)
    fulfilment_rate = completed_pos.count() / total_pos.count() * 100 if completed_pos.count() > 0 else 0
    fulfillment_rate = fulfilment_rate

    # Save updated metrics to the database
    hp = HistoricalPerformance(on_time_delivery_rate=round(on_time_delivery_rate, 2),
                               quality_rating_avg=round(quality_rating_avg, 2),
                               average_response_time=round(average_response_time),
                               fulfillment_rate=round(fulfillment_rate, 2),
                               vendor=po.vendor)
    hp.save()

    # Create HistoricalPerformance
    return on_time_delivery_rate


@receiver(post_save, sender=PurchaseOrder)
def purchase_order_status_changed(sender, instance, **kwargs):
    if instance.status == 'completed':
        calc_on_time_delivery_rate(instance)

# Incase you want to check only when the status is set to completed.
# @receiver(pre_save, sender=PurchaseOrder)
# def purchase_order_status_changed(sender, instance, **kwargs):
#     # Check if the status has changed to "completed"
#     if instance.pk is not None:
#         original_instance = PurchaseOrder.objects.get(pk=instance.pk)
#         if original_instance.status != instance.status and instance.status == 'completed':
#             calc_on_time_delivery_rate(instance)


# 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