# sublime-screeninfo


Sublime Text dependency of screeninfo for retrieving screen information.

Original Package:

* [GitHub](https://github.com/rr-/screeninfo)

Because of the lack of **dataclass**es in python 3.3, it returns a lambda instead.

### Usage

```python
from screeninfo import get_monitors, Enumerator
print("Native:")
for m in get_monitors():
	print(("\tMonitor "+m.name+" Position:"),m.x,"x",m.y)
	print(("\tMonitor "+m.name+" Size:"),m.width,"x",m.height)
	print(("\tMonitor "+m.name+" Size (mm):"),m.width_mm,"x",m.height_mm)
	print(("\tMonitor "+m.name+" DPI:"),m.dpiX,"x",m.dpiY)
print("Alternative driver:")
for m in get_monitors(Enumerator.Cygwin):
	print(("\tMonitor "+m.name+" Position:"),m.x,"x",m.y)
	print(("\tMonitor "+m.name+" Size:"),m.width,"x",m.height)
	print(("\tMonitor "+m.name+" Size (mm):"),m.width_mm,"x",m.height_mm)
	print(("\tMonitor "+m.name+" DPI:"),m.dpiX,"x",m.dpiY)
```

**Output**:

>Native:  
>	Monitor \\.\DISPLAY1 Position: 0 x 0  
>	Monitor \\.\DISPLAY1 Size: 1366 x 768  
>	Monitor \\.\DISPLAY1 Size (mm): 293 x 165  
>	Monitor \\.\DISPLAY1 DPI: 96 x 96  
>Alternative driver:  
>	Monitor \\.\DISPLAY1 Position: 0 x 0  
>	Monitor \\.\DISPLAY1 Size: 1366 x 768  
>	Monitor \\.\DISPLAY1 Size (mm): 293 x 165  
>	Monitor \\.\DISPLAY1 DPI: 96 x 96
