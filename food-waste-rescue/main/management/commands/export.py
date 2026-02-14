from main.models import Consumer, Seller, Bundle_posting, Reservation, IssueReport
from django.core.management.base import BaseCommand
from openpyxl import Workbook
import logging
from django.utils import timezone
import datetime

logger = logging.getLogger(__name__)

def tz_info_convert(attr):
    """Convert tz_info to None"""
    if isinstance(attr, datetime.datetime):
        if attr.tzinfo is not None:
            return timezone.localtime(attr).replace(tzinfo=None)
        return attr

    if isinstance(attr, datetime.time):
        if attr.tzinfo is not None:
            return attr.replace(tzinfo=None)
        return attr

    return attr

class Command(BaseCommand):
    help="Export database to an xlsx file."

    def handle(self, *args, **options):
        
        wb = Workbook()
        wb.remove(wb.active)
        models = [Consumer, Seller, Bundle_posting, Reservation, IssueReport]
        
        for model in models:
            ws = wb.create_sheet(model.__name__)
        
            fields = list(model._meta.fields)
            columns = []
            for field in fields:
                if field.is_relation:
                    columns.append(f"{field.name}_id")
                else:
                    columns.append(field.name)
            
            ws.append(columns)
            
            for object in model.objects.all():
                attributes = []
                for field in fields:
                    if field.is_relation:
                        attributes.append(tz_info_convert(getattr(object, field.attname)))
                    else:
                        attributes.append(tz_info_convert(getattr(object, field.name)))
                ws.append(attributes)
                
        wb.save("food_waste_rescue.xlsx")
        self.stdout.write("Saved food_waste_rescue.xlsx")
        

    
    