# Data Handler from AI task organized by Korea Customs Service

## Target Data
- Use
    - you should make a list
    - example
        - ```want_lists = ["Filename", "ImageID"]```
```want_lists = ["Filename", "RegisteredNumber"]
for want_list in want_lists :
    result.append(DataHandler.get_item(want_list))
print(result)```

## Data_split
- Use
    - example
        - split=True
- Not Use
    - example
        - split=False

## View Point
