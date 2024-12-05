#! /usr/bin/env python3

def page_order(order):
    pages = []
    for pair in order:
        for page in pair:
            pages.append(page)
    pages = list(set(pages))
    change = True
    while change:
        changes = 0
        for pair in order:
            a, b = pair
            i_a = pages.index(a)
            i_b = pages.index(b)
            if i_a > i_b:
                pages[i_a] = b
                pages[i_b] = a
                changes += 1
        if changes == 0:
            change = False

    return pages


def fix_order(series, pairs):
    change = True

    while change:
        changes = 0
        for pair in pairs:
            a, b = pair
            if a in series and b in series:
                i_a = series.index(a)
                i_b = series.index(b)
                if i_a > i_b:
                    series[i_a] = b
                    series[i_b] = a
                    changes += 1
        if changes == 0:
            change = False

    return series


def valid_order(series, pairs):
    for page in pairs:
        if page[0] in series and page[1] in series:
            if series.index(page[0]) > series.index(page[1]):
                return False
    return True


if __name__ == "__main__":
    with open("./puzzle.txt") as input_file:
        input_string = input_file.read()
    order, pages = input_string.split("\n\n")
    order = order.split("\n")
    order = [tuple(i.split('|')) for i in order]
    pages = pages.split('\n')
    score_1 = 0
    score_2 = 0
    for book in pages:
        book = book.split(',')
        if valid_order(book, order):
            i = int(book[len(book)//2])
            score_1 += i
        else:
            fix_order(book, order)
            j = int(book[len(book)//2])
            score_2 += j
    print(f"Part 1: {score_1}")
    print(f"Part 2: {score_2}")
