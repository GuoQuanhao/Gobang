thickarrow_strings = (  # sized 24x24
    "XX                      ",
    "XXX                     ",
    "XXXX                    ",
    "XX.XX                   ",
    "XX..XX                  ",
    "XX...XX                 ",
    "XX....XX                ",
    "XX.....XX               ",
    "XX......XX              ",
    "XX.......XX             ",
    "XX........XX            ",
    "XX........XXX           ",
    "XX......XXXXX           ",
    "XX.XXX..XX              ",
    "XXXX XX..XX             ",
    "XX   XX..XX             ",
    "     XX..XX             ",
    "      XX..XX            ",
    "      XX..XX            ",
    "       XXXX             ",
    "       XX               ",
    "                        ",
    "                        ",
    "                        ",
)

text_no = ("                        ",
           "                        ",
           "         XXXXXX         ",
           "       XX......XX       ",
           "      X..........X      ",
           "     X....XXXX....X     ",
           "    X...XX    XX...X    ",
           "   X.....X      X...X   ",
           "   X..X...X      X..X   ",
           "  X...XX...X     X...X  ",
           "  X..X  X...X     X..X  ",
           "  X..X   X...X    X..X  ",
           "  X..X    X.,.X   X..X  ",
           "  X..X     X...X  X..X  ",
           "  X...X     X...XX...X  ",
           "   X..X      X...X..X   ",
           "   X...X      X.....X   ",
           "    X...XX     X...X    ",
           "     X....XXXXX...X     ",
           "      X..........X      ",
           "       XX......XX       ",
           "         XXXXXX         ",
           "                        ",
           "                        ",
           )

text_arrow = ("xX                      ",
              "X.X                     ",
              "X..X                    ",
              "X...X                   ",
              "X....X                  ",
              "X.....X                 ",
              "X......X                ",
              "X.......X               ",
              "X........X              ",
              "X.........X             ",
              "X..........X            ",
              "X...X..X....X           ",
              "X..X     X...X          ",
              "X.X        X..X         ",
              "XX           X.X        ",
              "X              XX       ",
              "                        ",
              "                        ",
              "                        ",
              "                        ",
              "                        ",
              "                        ",
              "                        ",
              "                        ")

def compile(strings, black='X', white='.', xor='o'):
    size = len(strings[0]), len(strings)
    if size[0] % 8 or size[1] % 8:
        raise ValueError("cursor string sizes must be divisible by 8 %s" %
                         size)
    for s in strings[1:]:
        if len(s) != size[0]:
            raise ValueError("Cursor strings are inconsistent lengths")

    maskdata = []
    filldata = []
    maskitem = fillitem = 0
    step = 8
    for s in strings:
        for c in s:
            maskitem = maskitem << 1
            fillitem = fillitem << 1
            step = step - 1
            if c == black:
                maskitem = maskitem | 1
                fillitem = fillitem | 1
            elif c == white:
                maskitem = maskitem | 1
            elif c == xor:
                fillitem = fillitem | 1
            if not step:
                maskdata.append(maskitem)
                filldata.append(fillitem)
                maskitem = fillitem = 0
                step = 8
    return tuple(filldata), tuple(maskdata)


def load_xbm(curs, mask):
    def bitswap(num):
        val = 0
        for x in range(8):
            b = num & (1 << x) != 0
            val = val << 1 | b
        return val

    if type(curs) is type(''):
        with open(curs) as cursor_f:
            curs = cursor_f.readlines()
    else:
        curs = curs.readlines()

    if type(mask) is type(''):
        with open(mask) as mask_f:
            mask = mask_f.readlines()
    else:
        mask = mask.readlines()

    # avoid comments
    for line in range(len(curs)):
        if curs[line].startswith("#define"):
            curs = curs[line:]
            break
    for line in range(len(mask)):
        if mask[line].startswith("#define"):
            mask = mask[line:]
            break
    width = int(curs[0].split()[-1])
    height = int(curs[1].split()[-1])
    if curs[2].startswith('#define'):
        hotx = int(curs[2].split()[-1])
        hoty = int(curs[3].split()[-1])
    else:
        hotx = hoty = 0

    info = width, height, hotx, hoty

    for line in range(len(curs)):
        if curs[line].startswith('static char') or curs[line].startswith('static unsigned char'):
            break
    data = ' '.join(curs[line + 1:]).replace('};', '').replace(',', ' ')
    cursdata = []
    for x in data.split():
        cursdata.append(bitswap(int(x, 16)))
    cursdata = tuple(cursdata)

    for line in range(len(mask)):
        if mask[line].startswith('static char') or mask[line].startswith('static unsigned char'):
            break
    data = ' '.join(mask[line + 1:]).replace('};', '').replace(',', ' ')
    maskdata = []
    for x in data.split():
        maskdata.append(bitswap(int(x, 16)))
    maskdata = tuple(maskdata)
    return info[:2], info[2:], cursdata, maskdata
