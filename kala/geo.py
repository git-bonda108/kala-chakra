"""Location → latitude / longitude / timezone offset.

Offline first: a built-in table of common cities (India-heavy, plus a few
world capitals). Timezone offset is resolved with timezonefinder + zoneinfo
for the birth date (so historical DST is handled). Manual lat/lon/offset entry
is always available so the app never blocks on a lookup.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from timezonefinder import TimezoneFinder

    _TF = TimezoneFinder()
except Exception:  # pragma: no cover
    _TF = None


@dataclass
class Location:
    place: str
    lat: float
    lon: float
    tz_offset_hours: float
    tz_name: str = ""


# name -> (lat, lon). Keep display names human-friendly.
CITIES = {
    "Hyderabad, India": (17.3850, 78.4867),
    "Vijayawada, India": (16.5062, 80.6480),
    "Visakhapatnam, India": (17.6868, 83.2185),
    "Guntur, India": (16.3067, 80.4365),
    "Tirupati, India": (13.6288, 79.4192),
    "Rajahmundry, India": (17.0005, 81.8040),
    "Warangal, India": (17.9689, 79.5941),
    "Kakinada, India": (16.9891, 82.2475),
    "Nellore, India": (14.4426, 79.9865),
    "Kurnool, India": (15.8281, 78.0373),
    "Chennai, India": (13.0827, 80.2707),
    "Bengaluru, India": (12.9716, 77.5946),
    "Mumbai, India": (19.0760, 72.8777),
    "Delhi, India": (28.6139, 77.2090),
    "Kolkata, India": (22.5726, 88.3639),
    "Pune, India": (18.5204, 73.8567),
    "Ahmedabad, India": (23.0225, 72.5714),
    "Jaipur, India": (26.9124, 75.7873),
    "Lucknow, India": (26.8467, 80.9462),
    "Bhopal, India": (23.2599, 77.4126),
    "Nagpur, India": (21.1458, 79.0882),
    "Kochi, India": (9.9312, 76.2673),
    "Thiruvananthapuram, India": (8.5241, 76.9366),
    "Varanasi, India": (25.3176, 82.9739),
    "Patna, India": (25.5941, 85.1376),
    "Guwahati, India": (26.1445, 91.7362),
    "London, UK": (51.5074, -0.1278),
    "New York, USA": (40.7128, -74.0060),
    "San Francisco, USA": (37.7749, -122.4194),
    "Dubai, UAE": (25.2048, 55.2708),
    "Singapore": (1.3521, 103.8198),
    "Sydney, Australia": (-33.8688, 151.2093),
    "Toronto, Canada": (43.6532, -79.3832),
}

CITY_NAMES = sorted(CITIES.keys())


def tz_offset_for(lat: float, lon: float, when: datetime) -> tuple[float, str]:
    """Resolve UTC offset in hours for a coordinate at a given local datetime."""
    if _TF is not None:
        try:
            tzname = _TF.timezone_at(lat=lat, lng=lon)
            if tzname:
                tz = ZoneInfo(tzname)
                off = when.replace(tzinfo=tz).utcoffset()
                if off is not None:
                    return off.total_seconds() / 3600.0, tzname
        except Exception:
            pass
    # Fallback: India Standard Time for Indian longitudes, else UTC.
    if 68 <= lon <= 98 and 6 <= lat <= 37:
        return 5.5, "Asia/Kolkata (assumed)"
    return 0.0, "UTC (assumed)"


def resolve_city(name: str, when: datetime) -> Location | None:
    coords = CITIES.get(name)
    if not coords:
        return None
    lat, lon = coords
    off, tzname = tz_offset_for(lat, lon, when)
    return Location(name, lat, lon, off, tzname)
