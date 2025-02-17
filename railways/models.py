from django.db import models
from django.utils.timezone import now as timezone_now

# This model stores the API Keys required
# to access the admin panel, which proviedes
# admin to perform various functionalities like
# adding new train, updating seats, etc.
#
# For security concecerns, the API Keys are
# stored as SHA-256 hashes.
class AdminAPIKeys(models.Model):
    hashed_key = models.CharField(max_length=64, db_index=True)
    date_issued = models.DateTimeField(default=timezone_now, null=False)

