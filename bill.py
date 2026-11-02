# bill part

from datetime import datetime

from utils import (
    print_line,
    print_header,
    print_row,
    print_inform,
    format_money,
    format_quantity,
    LINE_WIDTH,
)

FIRST_ORDER_NO = 1001    # the first bill


def count_items(lines):
    total = 0
    for line in lines:
        total = total + line["quant"]
    return total


def count_lines(lines):
    return len(lines)


def calc_subtotal(lines):
    subtotal = 0
    i = 0
    while i < len(lines):
        subtotal = subtotal + lines[i]["price"] * lines[i]["quant"]
        i = i + 1
    return round(subtotal, 2)


def calc_total(subtotal):
    return round(subtotal, 2)


def calc_change(paid, total):
    change = round(paid - total, 2)
    if change < 0:
        return 0.0
    return change


def make_bill(lines):
    subtotal = calc_subtotal(lines)
    total = calc_total(subtotal)

    bill = {
        "lines": lines,
        "items": count_items(lines),
        "subtotal": subtotal,
        "total": total,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    return bill


def _amount_line(bill_line, money):
    label = "  " + str(bill_line)
    print(label.ljust(LINE_WIDTH - 14) + format_money(money).rjust(14))


def print_bill(bill, order_no, table_no, paid):
    change = calc_change(paid, bill["total"])

    print()
    print_line("=")
    print("RECEIPT".center(LINE_WIDTH))
    print_line("=")
    print(f"  Order No : {order_no}")
    print(f"  Table    : {table_no}")
    print(f"  Time     : {bill['time']}")

    print_header(["ID", "Name", "Price", "Qty", "Amount"])
    i = 0
    while i < len(bill["lines"]):
        line = bill["lines"][i]
        print_row(
            [
                line["id"],
                line["name"],
                format_money(line["price"]),
                format_quantity(line["quant"]),
                format_money(line["price"] * line["quant"]),
            ]
        )
        i = i + 1
    print_line("-")

    _amount_line(f"Subtotal ({bill['items']} item(s))", bill["subtotal"])
    print_line("-")
    _amount_line("TOTAL TO PAY", bill["total"])
    print_line("=")

    _amount_line("Paid", paid)
    _amount_line("Change", change)
    print_line("=")
    print("Thank you for dining with us!".center(LINE_WIDTH))
    print_line("=")

    return change


def print_bill_brief(bill, order_no):
    print_inform(
        f"Order {order_no}: {bill['items']} item(s), "
        f"subtotal {format_money(bill['subtotal'])}, "
        f"total {format_money(bill['total'])}."
    )