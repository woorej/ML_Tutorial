# Data Handler from AI task organized by Korea Customs Service

## Target Data
- Use
    - you should make a list
    - example
```
want_lists = ["Filename", "RegisteredNumber"]

for want_list in want_lists :
    result.append(DataHandler.get_item(want_list))
```

## Data_split
- Use
    - example
        - split=True
- Not Use
    - example
        - split=False
```
want_lists = ["Filename", "RegisteredNumber"]

for want_list in want_lists :
    result.append(DataHandler.get_item(want_list), split=True)
```

## View Point
- Use
    - example
        - view_point = [60, 90]
- Not Use
    - example
        - view_point = False
```
want_lists = ["Filename", "RegisteredNumber"]

for want_list in want_lists :
    result.append(DataHandler.get_item(want_list, split=False, view_point=[60, 90]))
```

