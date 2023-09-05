MS_HOUR = 3600000
MS_MIN = 60000
MS_SEC = 1000


def srt_time(time: int) -> str:
    """Gets a time in milliseconds and returns it as the subtitle time"""
    return f"{time // MS_HOUR:02}:{time // MS_MIN % 60:02}:{time // MS_SEC % 60:02},{time % MS_SEC:03}"
