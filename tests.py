from pkobfusticator import SplitOr, Obfusticator

TEST_NUMS = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    0xf,
    0xff,
    0xfff,
    0xffff,
    0xfffff,
    0xffffff,
    0xfffffff,
    0xffffffff,
]


class TestSplitMoreOr(object):
    def test_conversion(self):
        strategy = SplitOr(salt=0xc0de)
        key = 0x1234

        for num in TEST_NUMS:
            encoded = strategy.transcode(num, key=key)
            decoded = strategy.transcode(encoded, key=key)
            assert num == decoded, "Failed: %d" % num


class TestObfusticator(object):
    def test_base64(self):
        obfusticator = Obfusticator(strategy=SplitOr, salt=0xc0de)
        key = 0x1234

        for num in TEST_NUMS:
            encoded = obfusticator.to_base64(num, key=key)
            decoded = obfusticator.from_base64(encoded, key=key)

            assert num == decoded
