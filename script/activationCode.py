#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random, string

def generateCode(num, length):
    rawCode = string.ascii_letters + string.digits
    f = open('../activationCode', 'a')
    for i in range(num):
        codeList = [random.choice(rawCode) for j in range(length)]
        codeStr = ''.join(codeList) + '\n'
        f.write(codeStr)
    f.close()
    
def verifyCode(rawCode):
    f = open('../activationCode', 'r')
    codeList = f.read()
    flag = False
    for k in codeList.split():
        if k == rawCode:
            flag = True
    if flag:
        print('Congratulations! This code has been verified. ')
    else:
        print('Sorry. The code is invalid. ')
    f.close()
    
if __name__ == '__main__':
    num = int(input('Please input the number of activation codes you want. '))
    length = int(input('Please input the length of activation code you prefer. '))
    generateCode(num, length)
    # rawCode = input('Please input the code you want to verify. ')
    # verifyCode(rawCode)
