MS_HOUR = 3600000
MS_MIN = 60000
MS_SEC = 1000


def srt_time(time: int) -> str:
    """Gets a time in milliseconds and returns it as the subtitle time"""
    return f"{time // MS_HOUR:02}:{time // MS_MIN % 60:02}:{time // MS_SEC % 60:02},{time % MS_SEC:03}"


def srt_time_to_ms(time: str) -> int:
    """Gets a time in srt format and returns it in milliseconds"""
    return (
        int(time[:2]) * MS_HOUR
        + int(time[3:5]) * MS_MIN
        + int(time[6:8]) * MS_SEC
        + int(time[9:12])
    )
