"Setup class"

from distutils.core import setup

setup(
    name='ytdl',
    version='1.0.19',
    packages=['ytdl'],
    url='https://github.com/develohpanda/ytdl',
    description='YT download and upload to GMusic',
    install_requires=[
        'youtube-dl',
        'gmusicapi==10.1.2.rc1',
        'boto3',
        'mutagen',
        'configparser',
        'image',
        'google-api-python-client',
        'pytz'
    ],
    dependency_links=[
        'https://github.com/develohpanda/gmusicapi/tarball/develop#egg=gmusicapi-10.1.2rc1'
    ]
)
