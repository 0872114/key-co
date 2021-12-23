rus_chars = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
rus_levels = (256 // len(rus_chars))

en_chars = 'abcdefghijklmnopqrstuvwxyz'
en_levels = (256 // len(en_chars))

sym_chars = '.,?;:()\n=-!RESNJ'
sym_levels = (256 // len(sym_chars))

num_chars = '1234567890'
num_levels = 256 // len(num_chars)

emoji_chars = '🎈🪒'
emoji_levels = 256 // len(emoji_chars)

maps = dict(
    E={char: n * en_levels for n, char in enumerate(en_chars)},
    R={char: n * rus_levels for n, char in enumerate(rus_chars)},
    S={char: n * sym_levels for n, char in enumerate(sym_chars)},
    N={char: n * num_levels for n, char in enumerate(num_chars)},
    J={char: n * emoji_levels for n, char in enumerate(emoji_chars)},
)