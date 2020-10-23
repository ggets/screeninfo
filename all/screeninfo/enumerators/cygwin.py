import typing as T

def enumerate_monitors() -> T.Iterable[None]:
    import ctypes
    import ctypes.wintypes

    BOOL = ctypes.c_bool
    INT = ctypes.c_int
    HANDLE = ctypes.c_void_p
    HMONITOR = HANDLE
    HDC = HANDLE
    UINT = ctypes.c_uint
    LONG = ctypes.c_long
    ULONG = ctypes.c_ulong
    LONGLONG = ctypes.c_longlong
    ULONGLONG = ctypes.c_ulonglong
    DOUBLE = ctypes.c_double
    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", LONG),
            ("top", LONG),
            ("right", LONG),
            ("bottom", LONG),
        ]

    SPI_GETWORKAREA = 48
    CCHDEVICENAME = 32
    # gdi32.GetDeviceCaps keys for monitor size in mm
    HORZSIZE = 4
    VERTSIZE = 6

    user32 = ctypes.cdll.LoadLibrary("user32.dll")
    SPI = user32.SystemParametersInfoW

    ptr_size = ctypes.sizeof(HANDLE)
    if ptr_size == ctypes.sizeof(LONG):
        WPARAM = ULONG
        LPARAM = LONG
    elif ptr_size == ctypes.sizeof(LONGLONG):
        WPARAM = ULONGLONG
        LPARAM = LONGLONG

    MonitorEnumProc = ctypes.CFUNCTYPE(
        INT,
        HMONITOR,
        HDC,
        ctypes.POINTER(RECT),
        LPARAM
    )

    user32.EnumDisplayMonitors.argtypes = [
        HANDLE,
        ctypes.POINTER(RECT),
        MonitorEnumProc,
        LPARAM,
    ]
    user32.EnumDisplayMonitors.restype = BOOL

    class MONITORINFOEXW(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.wintypes.DWORD),
            ("rcMonitor", ctypes.wintypes.RECT),
            ("rcWork", ctypes.wintypes.RECT),
            ("dwFlags", ctypes.wintypes.DWORD),
            ("szDevice", ctypes.wintypes.WCHAR * CCHDEVICENAME),
        ]

    monitors = []

    def callback(monitor: T.Any, dc: T.Any, rect: T.Any, data: T.Any) -> int:
        info = MONITORINFOEXW()
        info.cbSize = ctypes.sizeof(MONITORINFOEXW)
        if ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            name = info.szDevice
        else:
            name = None

        h_size = ctypes.windll.gdi32.GetDeviceCaps(dc, HORZSIZE)
        v_size = ctypes.windll.gdi32.GetDeviceCaps(dc, VERTSIZE)

        rct = rect.contents

        SPI.restype = BOOL
        SPI.argtypes = [
            UINT,
            UINT,
            ctypes.POINTER(RECT),
            UINT
        ]
        rect = RECT()
        result = SPI(
            SPI_GETWORKAREA,
            0, 
            ctypes.byref(rect),
            0
        )

        cur_mon=lambda:None
        cur_mon.name=name
        cur_mon.x=rct.left
        cur_mon.y=rct.top
        cur_mon.width=(rct.right - rct.left)
        cur_mon.height=(rct.bottom - rct.top)
        cur_mon.width_mm=h_size
        cur_mon.height_mm=v_size
        if result:
            cur_mon.width_workarea=abs(rect.left-rect.right)
            cur_mon.height_workarea=abs(rect.top-rect.bottom)

        monitors.append(cur_mon)
        return 1

    # Make the process DPI aware so it will detect the actual
    # resolution and not a virtualized resolution reported by
    # Windows when DPI virtualization is in use.
    #
    # benshep 2020-03-31: this gives the correct behaviour on Windows 10 when
    # multiple monitors have different DPIs.
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    # On Python 3.8.X GetDC randomly fails returning an invalid DC.
    # To workaround this request a number of DCs until a valid DC is returned.
    for retry in range(100):
        # Create a Device Context for the full virtual desktop.
        dc_full = user32.GetDC(None)
        if dc_full > 0:
            # Got a valid DC, break.
            break
        user32.ReleaseDC(dc_full)
    else:
        # Fallback to device context 0 that is the whole
        # desktop. This allows fetching resolutions
        # but monitor specific device contexts are not
        # passed to the callback which means that physical
        # sizes can't be read.
        dc_full = 0
    # Call EnumDisplayMonitors with the non-NULL DC
    # so that non-NULL DCs are passed onto the callback.
    # We want monitor specific DCs in the callback.
    user32.EnumDisplayMonitors(
        dc_full,
        None,
        MonitorEnumProc(callback),
        0
    )
    user32.ReleaseDC(dc_full)

    yield from monitors
