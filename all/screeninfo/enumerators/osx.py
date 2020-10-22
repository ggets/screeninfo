import typing as T


def enumerate_monitors() -> T.Iterable[None]:
    from pyobjus import autoclass
    from pyobjus.dylib_manager import INCLUDE, load_framework

    load_framework(INCLUDE.AppKit)

    screens = autoclass("NSScreen").screens()

    for i in range(screens.count()):
        f = screens.objectAtIndex_(i).frame
        current_monitor=lambda: None
        if callable(f):
            f = f()

            current_monitor.x=int(f.origin.x)
            current_monitor.y=int(f.origin.y)
            current_monitor.width=int(f.size.width)
            current_monitor.height=int(f.size.height)

        yield current_monitor