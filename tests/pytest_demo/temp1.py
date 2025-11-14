import sys, os
import numpy as np

test_data1 = '''
1. Wow! That's amazing!
2. Help! I'm stuck!
'''

test_data2 = '''
1. Wow! That's amazing!
2. Help! I'm stuck!
3. No way! I can't believe it!
4. Great! That sounds fun!
5. What a surprise!
'''

test_data3 = [2, 99 , "Great", "!", 'That sounds fun!', 8, 8.88 , 200, 39.55, "ONE", "Two", "2341!%#$!@#4"]

def checkType(dType):
  if isinstance(dType, list):
    print("Var type = list")
  else:
    print("Var type is not a list, exit program")
    sys.exit()
  dTtype_len, poiNum = len(dType), 0
  print(dType, "Incoming data type is = ", type(dType), "has the length = ",dTtype_len)
  for var in dType:
    print(f"Index position at: {poiNum}; Variable value = {var},  Type: {type(var)}")
    poiNum = poiNum+1
  whatType = str(type(dType))
  print("1 = ", dType, dType[::-1], dType[3])
  print("2 = ", whatType, whatType[8:12])
  b = [2, 99 , "Great", "!", 'That sounds fun!', 8, 8.88 , 200, 39.55, "ONE", "Two", "2341!%#$!@#4"]
  print(b, type(b))
  for i in b:
    poiNum = 0
    print(f"at {poiNum+1} value = {i}")
  b = str(b)
  print(b, type(b))
  for i in b:
    poiNum = 0
    # print(f"at {poiNum+1} value = {i}")


def checkData(dData):
  print("Incoming data type is = ", type(dData))
  for var in dData:
    print(f"Variable: {var}, Type: {type(var)}")
  print()

# checkType(test_data3)
checkType(test_data3)
# checkData(test_data2)
# print(test_data3[2:5], (test_data3[2:5])[::-1])
