from django.utils import timezone
from .models import Rental
from .celery import app


@app.task
def calculate_rental_cost(rental_id):
    try:
        rental = Rental.objects.get(id=rental_id)
        rental.end_time = timezone.now()
        rental.total_cost = (
            rental.end_time - rental.start_time).total_seconds() / 3600 * 300
        rental.save()
        return f'Rental {rental_id} cost calculated successfully.'
    except Rental.DoesNotExist:
        return f'Rental {rental_id} does not exist.'
