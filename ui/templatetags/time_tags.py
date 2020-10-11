"""
Timetag templatestags.
"""

# Django
from django import template

# Utilities
from datetime import datetime

# Register
register = template.Library()


@register.filter
def human_timestamp_duration(timestamp):
    """
    Gets a timestamp duration
    an returns a timestamp
    readable for a human.
    """

    if not timestamp:
        return 'Unknow'

    try:
        raw_timestamp = datetime.fromtimestamp(timestamp)
        duration = raw_timestamp.strftime('%Hh %Mm')

    except ValueError:
        return None

    if duration == '00:00:00':
        return 'Unknow'

    return duration


@register.filter
def human_timestamp_date(timestamp):
    """
    Gets a timestamp date
    an returns a timestamp
    readable for a human.
    """

    try:
        raw_timestamp = datetime.fromtimestamp(timestamp)
        date = raw_timestamp.strftime('%Y-%m-%d')

    except ValueError:
        return None

    return date


@register.filter
def human_milliseconds(milliseconds):
    """
    Gets the milliseconds an returns
    a time readable for a human.
    """

    try:
        ms = int(milliseconds)
        raw_seconds = (ms / 1000) % 60
        raw_minutes = (ms / (1000 * 60)) % 60
        seconds = str(raw_seconds).split('.')
        minutes = str(raw_minutes).split('.')

    except ValueError:
        return None

    return '{}m {}s'.format(minutes[0], seconds[0])


@register.filter
def name_url(url):
    """
    Gets an url an returns
    the short name of the url.
    """

    try:
        split_url = url.split('/')
        split_name = split_url[2].split('.')

        if len(split_name) == 2:
            name = split_name[0]

        elif len(split_name) == 3:
            name = split_name[1]

        elif len(split_name) == 4:
            name = split_name[2]

    except IndexError:
        return 'Unknow'

    return name


@register.filter
def count_seasons(seasons):
    """
    Get an array of seasons
    and returns the total.
    """

    try:
        count = len(list(seasons))

    except ValueError:
        return None

    return count


@register.filter
def add_comma(array):
    """
    Get an array an returns
    a string of it separated
    in commas.
    """

    try:
        raw_text = ''

        for item in array:
            raw_text += '{}, '.format(item['name'])

        text = raw_text.rstrip(', ')

    except IndexError:
        return array

    return text
