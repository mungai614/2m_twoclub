from django.core.management.base import BaseCommand
from winnieclubapp.models import StockItem
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Check stock levels and send email alerts for low stock'

    def handle(self, *args, **kwargs):
        low_stock_items = StockItem.objects.filter(quantity__lte=models.F('min_stock_level'))
        if low_stock_items.exists():
            message_lines = []
            for item in low_stock_items:
                line = f"{item.name} - Quantity: {item.quantity} (Min Level: {item.min_stock_level})"
                message_lines.append(line)

            message = "\n".join(message_lines)
            self.stdout.write("Low stock alert for following items:\n" + message)

            # Send email alert
            send_mail(
                subject="Low Stock Alert",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin[1] for admin in settings.ADMINS],
                fail_silently=False,
            )
        else:
            self.stdout.write("All stock levels are sufficient.")
