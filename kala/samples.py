"""Sample nativities for quick trials and the eval harness.

GR-001 is the externally-verified golden case from the handover. The others are
representative mock nativities used to demonstrate the UI and to freeze
regression snapshots in the eval harness.
"""

from __future__ import annotations

from kala.chart import Native

SAMPLES: dict[str, Native] = {
    "Satya Anand (GR-001)": Native(
        name="Satya Anand Bonda",
        date="1977-11-25",
        time="01:55:00",
        tz_offset_hours=5.5,
        lat=22.5726,
        lon=88.3639,
        place="Kolkata, India",
    ),
    "2013 Friday sheet": Native(
        name="2013 Friday sheet",
        date="2013-11-08",
        time="05:59:00",
        tz_offset_hours=5.5,
        lat=17.3850,
        lon=78.4867,
        place="Hyderabad, India (place inferred)",
    ),
    "Demo — Chennai 1992": Native(
        name="Anita Rao",
        date="1992-03-14",
        time="09:20:00",
        tz_offset_hours=5.5,
        lat=13.0827,
        lon=80.2707,
        place="Chennai, India",
    ),
    "Demo — Delhi 1985": Native(
        name="Rohan Mehta",
        date="1985-08-20",
        time="22:10:00",
        tz_offset_hours=5.5,
        lat=28.6139,
        lon=77.2090,
        place="Delhi, India",
    ),
}
