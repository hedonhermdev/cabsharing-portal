from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from main.utils import find_overlap_range, find_max_overlap_range


LOCATION_CHOICES = (
    ("PIL", "PILANI"),
    ("LOH", "LOHARU"),
    ("DEL", "DELHI"),
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

    def save(self):
        if self.group:
            super().save()

        self_range = (self.start, self.end)
        groups = Group.objects.filter(
            to_location=self.to_location,
            from_location=self.from_location,
            is_full=False,
        )

        # No groups available, put listing in a new group
        if groups.count() == 0:
            g = Group(to_location=self.to_location,
                      from_location=self.from_location,
                      start=self.start,
                      end=self.end)
            self.group = g
        else:
            list_of_ranges = [(g.start, g.end) for g in groups]
            max_range = find_max_overlap_range(self_range, list_of_ranges)
            best_group = groups[list_of_ranges.index(max_range)]
            overlap = find_overlap_range(self_range, max_range)
            if overlap:
                self.group = best_group
                self.group.start = overlap[0]
                self.group.end = overlap[1]
            else:
                g = Group(to_location=self.to_location,
                          from_location=self.from_location,
                          start=self.start,
                          end=self.end)
                self.group = g
        self.group.save()
        super().save()

    def to_dict(self):
        return {
            'pk': self.pk,
            'lister': self.lister.pk,
            'group': self.group.pk,
            'to_location': self.to_location,
            'from_location': self.from_location,
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
        }

    def __str__(self):
        return f"Listing({self.lister}, {self.to_location}, {self.from_location})"


class GroupManager(models.Manager):
    def fav_groups(self,to_location,from_location):
        return super(GroupManager,self).get_query_set().filter(is_full=False,to_location=to_location,from_location=from_location)



class Group(models.Model):

    MAX_MEMBERS = 4

    to_location = models.CharField(choices=LOCATION_CHOICES, max_length=3)
    from_location = models.CharField(choices=LOCATION_CHOICES, max_length=3)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_full = models.BooleanField(default=False)

    get = GroupManager()

    def save(self):
        if self.members.count() == self.MAX_MEMBERS:
            self.is_full = True
        super().save()

    def to_dict(self):
        return {
            'pk': self.pk,
            'to_location': self.to_location,
            'from_location': self.from_location,
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),
            'members': [m.to_dict() for m in self.members.all()],
            'is_full': self.is_full,
        }

    def __str__(self):
        return f"Group({self.to_location}, {self.from_location})"

