from collections import namedtuple 

TrackRecord = namedtuple('TrackRecord', [
    'channel',
    'title', 
    'artist',
    'url', 
    'timestamp'
])