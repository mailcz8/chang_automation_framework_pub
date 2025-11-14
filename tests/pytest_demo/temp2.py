import pytest

def monkey_trouble(a_smile, b_smile):
    # return a_smile==b_smile==True or a_smile==b_smile==False
    text = "14.644"
    res = a_smile==b_smile==True
    print("Expected: " + str(res), float(text))
    return res

monkey_trouble(True, True)

