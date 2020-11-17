# Tools to help with collecting data from a string

# Get a substring within a string, where it checks between two strings, from a specific index. 
def getString(text, beginName, endName, fromIndex, startValue = 0, endValue = 0) :
    startIndex = text.index(beginName, fromIndex) + startValue
    endIndex = text.index(endName, startIndex) + endValue

    return text[startIndex : endIndex]

# Same as previous but checking from the bottom to the top
def getStringReverse(text, beginName, endName, startValue = 0, endValue = 0) :
    endIndex = text.rindex(endName) + endValue
    startIndex = text.rindex(beginName) + startValue

    return text[startIndex : endIndex]

    