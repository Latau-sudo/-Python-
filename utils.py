# utils part
# print、format

CURRENCY = "¥"          
LINE_WIDTH = 70

# 列数，宽度之和为 LINE_WIDTH
LAYOUTS = {
    2: ([40, 29], ["l", "r"]),
    3: ([36, 18, 14], ["l", "r", "r"]),
    4: ([6, 30, 18, 13], ["l", "l", "l", "r"]),
    5: ([6, 28, 10, 10, 12], ["l", "l", "r", "r", "r"]),
    6: ([5, 22, 10, 8, 8, 12], ["l", "l", "r", "r", "r", "r"]),
}


def print_line(text="-", width=LINE_WIDTH):

    if len(text) == 1:
        print(text * width)
    else:
        print(text)


def print_title(title, upper=True):
    text = str(title)
    if upper:
        text = text.upper()
    print()
    print_line("=")
    print(text.center(LINE_WIDTH))
    print_line("=")


def print_section(title):
    
    print()
    print_line("-")
    print("  " + str(title))


def _layout(column_count):
    
    if column_count in LAYOUTS:
        return LAYOUTS[column_count]

    width = LINE_WIDTH // column_count - 1
    widths = [width] * column_count
    aligns = ["l"] * (column_count - 1) + ["r"]
    return widths, aligns


def _cell(value, width, align):
    text = str(value)
    if len(text) > width:
        if width > 3:
            text = text[:width - 3] + "..."
        else:
            text = text[:width]

    if align == "r":
        return text.rjust(width)
    else:
        return text.ljust(width)


def _join(values, widths, aligns):
    cells = []
    i = 0
    while i < len(values) and i < len(widths):
        cells.append(_cell(values[i], widths[i], aligns[i]))
        i = i + 1
    return " ".join(cells)


def print_header(columns):
    widths, aligns = _layout(len(columns))
    print_line("-")
    print(_join(columns, widths, aligns))
    print_line("-")


def print_row(values):
    widths, aligns = _layout(len(values))
    print(_join(values, widths, aligns))


def print_warning(text):
    print(f"[!] {text}")


def print_success(text):
    print(f"[OK] {text}")


def print_inform(text):
    print(f"[i] {text}")


def format_money(money):
    # 15 -> "¥15.00"
    return f"{CURRENCY}{money:,.2f}"


def format_quantity(number):
    # 3.0 -> "3"
    if isinstance(number, float) and number == int(number):
        return str(int(number))
    return str(number)


def clean_text(text):
    return str(text).strip()


def read_text(prompt, allow_empty=False):
    while True:
        text = clean_text(input(prompt))
        if text != "" or allow_empty:
            return text
        print_warning("Input can not be empty.")


def read_int(prompt, min_value=None, max_value=None):
    # 输入字母、超范围都会被重问
    while True:
        text = clean_text(input(prompt))

        if text == "":
            print_warning("Please type a number.")
            continue

        try:
            number = int(text)
        except ValueError:
            print_warning(f"'{text}' is not a whole number, please try again.")
            continue

        if min_value is not None and number < min_value:
            print_warning(f"The number can not be less than {min_value}.")
            continue

        if max_value is not None and number > max_value:
            print_warning(f"The number can not be more than {max_value}.")
            continue

        return number


def read_float(prompt, min_value=None, max_value=None):
    while True:
        text = clean_text(input(prompt))

        if text == "":
            print_warning("Please type a number.")
            continue

        try:
            number = float(text)
        except ValueError:
            print_warning(f"'{text}' is not a number, please try again.")
            continue

        if min_value is not None and number < min_value:
            print_warning(f"The number can not be less than {min_value}.")
            continue

        if max_value is not None and number > max_value:
            print_warning(f"The number can not be more than {max_value}.")
            continue

        return number


def read_yes_no(prompt):
    while True:
        text = clean_text(input(prompt)).lower()
        if text in ("y", "yes"):
            return True
        if text in ("n", "no"):
            return False
        print_warning("Please answer y or n.")