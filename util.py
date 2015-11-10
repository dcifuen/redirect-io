import os

import constants


def get_environment():
    """
    Returns the environment based on the OS variable server software
    :return: The current environment that the app is running on
    """

    # Auto-set settings object based on App Engine dev environ

    if 'SERVER_SOFTWARE' in os.environ:
        if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
            return constants.ENV_LOCAL
        elif os.environ['SERVER_SOFTWARE'].startswith('Google App Engine/'):
            return constants.ENV_PRODUCTION
    # Should not happen
    return constants.ENV_LOCAL
