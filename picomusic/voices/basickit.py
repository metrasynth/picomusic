from .sunvoxvoice import SunvoxVoice
from ..tunings import drumkit


class BasicKit(SunvoxVoice):
    """A basic drum kit."""

    default_tuning = drumkit
