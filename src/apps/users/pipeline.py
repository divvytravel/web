# -*- coding: utf-8 -*-

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_facebook_birthday(response):
    birthday = response.get('birthday', None)
    if birthday:
        try:
            birthday = datetime.strptime(birthday, "%m/%d/%Y").date()
        except ValueError:
            logger.warning(
                "Unknown facebook birthday format: '{0}'".format(birthday))
            birthday = None
    return birthday


def store_additional_fields(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        birthday = get_facebook_birthday(response)
        if birthday:
            user.birthday = birthday
        user.save()