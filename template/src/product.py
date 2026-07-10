"""Product code lives here. The scaffold ships one health probe wired to
AC-1 so the AC -> test -> gate chain demonstrates green out of the box."""


def health() -> str:
    return "ok"
