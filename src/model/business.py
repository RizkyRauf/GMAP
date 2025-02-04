from dataclasses import dataclass

@dataclass
class Business:
    """Holds business data from Google Maps"""
    name: str = None
    address: str = None 
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None
    map_url: str = None
