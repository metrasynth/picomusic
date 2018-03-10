from ..tunings import drumkit
from .sunvoxvoice import SunvoxVoice


class BasicKit(SunvoxVoice):
    """A basic drum kit."""

    default_tuning = drumkit
