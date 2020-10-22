import typing as T


def enumerate_monitors() -> T.Iterable[None]:
    import ctypes

    LONG = ctypes.c_int32
    BOOL = ctypes.c_int
    HANDLE = ctypes.c_void_p
    HMONITOR = HANDLE
    HDC = HANDLE

    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", LONG),
            ("top", LONG),
            ("right", LONG),
            ("bottom", LONG),
        ]

    user32 = ctypes.cdll.LoadLibrary("user32.dll")

    ptr_size = ctypes.sizeof(ctypes.c_void_p)
    if ptr_size == ctypes.sizeof(ctypes.c_long):
        WPARAM = ctypes.c_ulong
        LPARAM = ctypes.c_long
    elif ptr_size == ctypes.sizeof(ctypes.c_longlong):
        WPARAM = ctypes.c_ulonglong
        LPARAM = ctypes.c_longlong

    MonitorEnumProc = ctypes.CFUNCTYPE(
        BOOL, HMONITOR, HDC, ctypes.POINTER(RECT), LPARAM
    )

    user32.EnumDisplayMonitors.argtypes = [
        HANDLE,
        ctypes.POINTER(RECT),
        MonitorEnumProc,
        LPARAM,
    ]
    user32.EnumDisplayMonitors.restype = ctypes.c_bool

    monitors = []

    def callback(monitor: T.Any, dc: T.Any, rect: T.Any, data: T.Any) -> int:
        rct = rect.contents
        current_monitor=lambda:None

        current_monitor.x=rct.left
        current_monitor.y=rct.top
        current_monitor.width=rct.right - rct.left
        current_monitor.height=rct.bottom - rct.top

        monitors.append(current_monitor)
        return 1

    user32.EnumDisplayMonitors(None, None, MonitorEnumProc(callback), 0)

    yield from monitors
