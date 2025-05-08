def validate_coords(lat:float, long:float) -> None:
    # Validates the lat and long are within the correct ranges.
    if(lat < -90 or lat > 90):
        raise ValueError("Latitude must be range -90 to 90 degrees.")

    if(long < -180 or long > 180):
        raise ValueError("Longitude must be in range -180 to 180 degrees.")