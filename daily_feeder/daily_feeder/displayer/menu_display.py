from daily_feeder.printer.lcd import print

max_display = 3

def display(header, items, selected_index):
    min_index = 0
    if selected_index - max_display >= 0:
        min_index = selected_index - max_display + 1
        selected_index = max_display - 1

    print_items = []
    for item in enumerate(items[min_index:min_index+max_display]):
        index = item[0]
        text = item[1]
        if selected_index == index:
            text = "> " + text
        else:
            text = "  " + text
        print_items.append(text)

    print(header, print_items)
