import os


def get_version(request):
    """Process docker image version from version.txt"""

    if os.environ.get('VERSION') is None:
        try:
            file = open('version.txt', 'r')
            version = file.read()
            file.close()
        except FileNotFoundError:
            version = 'DEV'

        if version == '':
            os.environ['VERSION'] = 'DEV'
        else:
            os.environ['VERSION'] = version

    return {'version': os.environ.get('VERSION')}
