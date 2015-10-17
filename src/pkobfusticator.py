import base64
import struct


class BaseStrategy(object):
    def transcode(self, num, key):
        """Convert num from one form to another"""
        raise NotImplementedError()

    def __call__(self, num, key):
        """Simple proxy to transcode"""
        return self.transcode(num, key)


class SplitExclusiveOr(BaseStrategy):
    """Use one portion of our number to encode the other"""
    def __init__(self, salt):
        self.salt = salt

    def transcode(self, num, key):
        right = num & 0xffff
        left = num >> 16 & 0xffff

        encoded_left = left ^ self.transform(right, key)
        encoded_right = right ^ self.transform(encoded_left, key)

        return (encoded_right << 16) + encoded_left

    def transform(self, num, key):
        """Encode a 16-bit integer"""
        encoded = (num ^ key) * self.salt
        return encoded & 0xffff


class Obfusticator(object):
    """Primary interface for obfusticating integers.

    Any strategy that implements the `BaseStrategy` interface can be
    used.
    """
    def __init__(self, strategy, salt):
        self.strategy = strategy(salt=salt)

    def transcode(self, num, key):
        return self.strategy(num, key)

    def to_base64(self, num, key):
        """Transcode an integer and encode in Base64.

        This is useful for URL friendliness.
        """
        encoded = self.transcode(num, key=key)
        as_bytes = struct.pack('!L', encoded)
        as_string = base64.b64encode(as_bytes)

        # Encoding Base64 usually converts three bytes to four
        # characters. However if there is a remainder we append a
        # trailer to our base64 to indicate that that chunk represents
        # fewer bytes. This trailer consists of "=" symbols with one "="
        # meaning two bytes, and "==" meaning one byte/
        #
        # As we're dealing with 32-bit ints, we'll have 4 bytes. As,
        # 4 % 3 == 1, we will *always* have a trailer of "==", so we can
        # remove it here and add it back in when we decode.
        truncated = as_string[:-2]
        return truncated

    def from_base64(self, encoded, key):
        """Return a Base64 string to it's original PK."""
        # See `to_base64` comment for explanation for appending a
        # padding
        encoded += b'=='
        as_string = base64.b64decode(encoded)

        as_bytes = struct.unpack('!L', as_string)[0]
        return self.transcode(as_bytes, key=key)


def get_defualt_obfusticator(salt):
    """Small helper to fetch the correct obfusticator"""
    return Obfusticator(SplitExclusiveOr, salt)
