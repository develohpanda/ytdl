from distutils.core import setup

setup(
    name='ytdl',
    version='1.0.0',
    packages=['ytdl'],
    url='https://github.com/develohpanda/ytdl',
    description='YT download and upload to GMusic',
    install_requires=[
        "youtube-dl",
        "gmusicapi",
    ],
)