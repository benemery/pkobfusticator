# PkObfusticator

![Build status]
(https://travis-ci.org/benemery/pkobfusticator.svg?branch=master)

Simple Primary Key obfustication so they can be referenced publically without revealing information about the system behind it.


## Usage

    from pkobfusticator import get_defualt_obfusticator

    pk_obfusticator = get_defualt_obfusticator(salt=0x1234)

    as_base64 = pk_obfusticator.to_base64(num=12345, key='foobar')

    # ... expose to the user ...

    as_int = pk_obfusticator.from_base64(encoded=as_base64, key='foobar')

    assert as_int == 12345
