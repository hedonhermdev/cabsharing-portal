from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from main.utils import find_overlap_range, find_max_overlap_range


LOCATION_CHOICES = (
    ("PIL", "PILANI"),
    ("LOH", "LOHARU Railway Station"),
    ("IGI", "Delhi Airport"),
    ("NDL", "New Delhi Railway Station"),
    ("JAI", "JAIPUR"),
)


class Listing(models.Model):
    lister = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    group = models.ForeignKey(
        "Group", related_name="members", on_delete=models.CASCADE, null=True, blank=True
    )
    to_location = models.CharField(choices=LOCATION_CHOICES, max_length=3)
    from_location = models.CharField(choices=LOCATION_CHOICES, max_length=3)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def to_dict(self):
        if self.group is None:
            group_info = None
        else :
            group_info = self.group.pk
        return {
            "pk": self.pk,
            "lister": self.lister.pk,
            "group": group_info,
            "to_location": self.to_location,
            "from_location": self.from_location,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
        }

    def __str__(self):
        return f"Listing({self.lister}, {self.to_location}, {self.from_location})"


class GroupManager(models.Manager):
    def groups_by_dest(self, to_location, from_location):
        return self.filter(to_location=to_location, from_location=from_location)


class Group(models.Model):

    MAX_MEMBERS = 4

    to_location = models.CharField(choices=LOCATION_CHOICES, max_length=3)
    from_location = models.CharField(choices=LOCATION_CHOICES, max_length=3)
    start = models.DateTimeField()
    end = models.DateTimeField()
    # Saving this to the database rather than making it a property method so that I can filter using this flag.
    is_full = models.BooleanField(default=False)

    objects = GroupManager()

    def save(self):
        if self.members.count() == self.MAX_MEMBERS:
            self.is_full = True
        super().save()

    def to_dict(self):
        return {
            "pk": self.pk,
            "to_location": self.to_location,
            "from_location": self.from_location,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "members": [m.to_dict() for m in self.members.all()],
            "is_full": self.is_full,
        }

    def __str__(self):
        return f"Group({self.to_location}, {self.from_location})"
