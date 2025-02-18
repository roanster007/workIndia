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
    hashed_key = models.CharField(max_length=64, db_index=True, unique=True)
    date_issued = models.DateTimeField(default=timezone_now, null=False)


class User(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=30)
    auth_token = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    token_issued = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["email", "password"],
                name="email_pass_index",
            ),
        ]


# Each train is assumed to have a fixed path.
# The source and destination are stored in the
# form of the indices / ids of the nodes / stations
# in that path.
class Train(models.Model):
    source = models.PositiveIntegerField()
    destination = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone_now, null=False)

    class Meta:
        indexes = [
            models.Index(
                fields=["source", "destination"],
                name="source_destination_index",
            ),
            models.Index(
                fields=["id"],
                name="trains_id_index",
            ),
        ]
    
    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "destination": self.destination,
            "seats": self.seats
        }


class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    source = models.PositiveIntegerField()
    destination = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    status = models.IntegerField(null=True)
    date = models.DateTimeField(default=timezone_now, null=False)

    PENDING = 0
    CONFIRMED = 1
    # TODO: Pick a better name for it
    CANCELLED = 2

    class Meta:
        indexes = [
            models.Index(
                fields=["user"],
                name="user_id_index",
            ),
            models.Index(
                fields=["train"],
                name="train_id_index",
            ),
            models.Index(
                fields=["id", "user"],
                name="book_id_user_index",
            ),
            models.Index(
                fields=["train", "source", "destination"],
                name="train_source_dest_index",
            ),
        ]

    def to_dict(self):
        return {
            "user_id": self.user.id,
            "train": self.train.id,
            "source": self.source,
            "destination": self.destination,
            "seats": self.seats,
            "status": self.status,
            "id": self.id,
        }
