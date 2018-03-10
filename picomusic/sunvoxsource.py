import ctypes

import sunvox.api as sv
from pyglet.media import AudioData, AudioFormat, StreamingSource

_BUFFERS = {}


class SunvoxSource(StreamingSource):
    """A bridge between the SunVox library and Pyglet audio playback."""

    def __init__(self, api, freq, channels, bytes_per_sample) -> None:
        """
        :param api: Instance of the SunVox API to use for audio rendering.
        :param freq: Frequency, as frames per second.
        :param channels: Channels (1=mono, 2=stereo).
        :param bytes_per_sample: Bytes per sample
            (2=16-bit int, 4=32-bit float).
        """
        super().__init__()
        self.audio_format = AudioFormat(channels, bytes_per_sample * 8, freq)
        self.sunvox = api
        self._duration = 0.
        self._tell = 0
        self._freq = freq
        self._channels = channels
        self._bytes_per_sample = bytes_per_sample
        self._bytes_per_second = freq * bytes_per_sample * channels

    def get_audio_data(self, bytes) -> (AudioData, None):
        offset = self._tell
        timestamp = float(offset) / self._bytes_per_second
        # Align to sample size
        if self._bytes_per_sample == 2:
            bytes &= 0xfffffffe
        elif self._bytes_per_sample == 4:
            bytes &= 0xfffffffc
        if bytes in _BUFFERS:
            buffer, byref = _BUFFERS[bytes]
        else:
            buffer = ctypes.create_string_buffer(bytes)
            byref = ctypes.byref(buffer)
            _BUFFERS[bytes] = buffer, byref
        frames = bytes // self._bytes_per_sample // self._channels
        self.sunvox.audio_callback(byref, frames, 0, self.sunvox.get_ticks())
        self._tell += bytes
        data = buffer.raw
        if not len(data):
            return None
        duration = float(len(data)) / self._bytes_per_second
        return AudioData(data, len(data), timestamp, duration, [])


def inprocess_sunvox_source() -> SunvoxSource:
    """
    :return: A SunvoxSource configured to render in the current process.
    """
    flags = (sv.SV_INIT_FLAG.ONE_THREAD |
             sv.SV_INIT_FLAG.AUDIO_INT16 |
             sv.SV_INIT_FLAG.USER_AUDIO_CALLBACK |
             sv.SV_INIT_FLAG.NO_DEBUG_OUTPUT)
    freq = 44100
    channels = 2
    bytes_per_sample = 2
    sv.init(None, freq, channels, flags)
    return SunvoxSource(sv, freq, channels, bytes_per_sample)
