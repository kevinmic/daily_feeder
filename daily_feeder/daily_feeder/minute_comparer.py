class InRange:
    def __init__(self, start, end):
        self._range = range(start,end)

    def __contains__(self, item):
        hours = int(item / 60 / 24)
        item = item - (hours * 24 * 60)
        return item in self._range

    def __repr__(self):
        return f"{self._range}"


class NotInRange(InRange):
    def __contains__(self, item):
        return not super().__contains__(item)

    def __repr__(self):
        return f"NOT {super().__repr__()}"


class AllRange:
    def __contains__(self, item):
        return True

    def __repr__(self):
        return "range(ANY)"

def allowed_minutes_checker(start, end):
    if start < end:
        return InRange(start, end)
    elif start == end:
        return AllRange()
    else:
        return NotInRange(end, start)