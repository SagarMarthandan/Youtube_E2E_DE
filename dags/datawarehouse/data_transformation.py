from datetime import timedelta, datetime


def parse_duration(duration_str):
    """
    Parses an ISO 8601 duration string (e.g., 'PT1H2M10S') into a timedelta object.
    
    Args:
        duration_str (str): The ISO 8601 duration string to parse.
        
    Returns:
        datetime.timedelta: A timedelta object representing the parsed duration.
    """
    
    duration_str = duration_str.replace("P", "").replace("T", "")
    components = ["D", "H", "M", "S"]
    values = {"D": 0, "H": 0, "M": 0, "S": 0}

    for component in components:
        if component in duration_str:
            value, duration_str = duration_str.split(component)
            values[component] = int(value)

    total_duration = timedelta(
        days=values["D"], hours=values["H"], minutes=values["M"], seconds=values["S"]
    )

    return total_duration


def transform_data(row):
    """
    Transforms the data row by formatting the duration and classifying the video type.
    
    Converts the 'Duration' from an ISO 8601 string into a standard Python `time` object.
    Additionally, it creates a new key 'Video_Type', classifying the video as 'Shorts' 
    if the duration is 60 seconds or less, and 'Normal' otherwise.
    
    Args:
        row (dict): A dictionary representing a single row of video data, containing at least a 'Duration' key.
        
    Returns:
        dict: The modified row dictionary with the updated 'Duration' and new 'Video_Type' key.
    """
    duration_td = parse_duration(row["Duration"])
    row["Duration"] = (datetime.min + duration_td).time()
    row["Video_Type"] = "Shorts" if duration_td.total_seconds() <= 60 else "Normal"
    return row