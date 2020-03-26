import datetime
from django.core.validators import ValidationError


def find_num_hours(dt_range):
    return (dt_range[1] - dt_range[0]).seconds // 3600


def find_overlap_range(range1, range2):
    """
    Given two datetime ranges find range of overlap between the two ranges
    :param range1: A tuple of two datetime objects (start, end)
    :param range2: A tuple of two datetime objects (start, end)
    :return: A tuple of two datetime objects (start, end)
    """
    start1 = range1[0]
    end1 = range1[1]
    start2 = range2[0]
    end2 = range2[1]

    # Range1 == Range2 
    if start1 == start2 and end1==end2:
        return start1, end1
    # One range ends before other range begins. Overlap is 0
    if end1 <= start2 or end2 <= start1:
        return None
    # range2 belongs to range1
    elif start1 <= start2 < end2 <= end1:
        return range2
    # range1 belongs to range2
    elif start2 <= start1 < end1 <= end2:
        return range1
    # range1 starts before range2
    elif start1 <= start2 < end1 <= end2:
        return start2, end1
    # range2 starts before range1
    elif start2 <= start2 < end2 <= end1:
        return start1, end2


def find_num_hours_in_overlap(range1, range2):
    overlap_range = find_overlap_range(range1, range2)
    if overlap_range == None:
        return 0
    return find_num_hours(overlap_range)


def find_max_overlap_range(range1, list_of_ranges):
    return sorted(list_of_ranges, key=lambda r: find_num_hours_in_overlap(range1, r))[-1]


def validate(instance, json_data):
    if hasattr(instance, "validators"):
        validators = getattr(instance, "validators")
        for validator in validators:
            validator(json_data)
    return True
