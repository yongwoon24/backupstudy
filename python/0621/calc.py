def calc(num1, num2, op):
    if op == '+':
        return num1+num2
    elif op == '-':
        return num1-num2
    elif op == '*':
        return num1*num2
    elif op == '/':
        return num1/num2
    elif op == '%':
        return num1%num2
    elif op == '//':
        return num1//num2

def calc2(num1, num2, op):
    match op:
        case '+':
            return num1+num2
        case '-':
            return num1-num2
        case '*':
            return num1*num2
        case '/':
            return num1/num2
        case '%':
            return num1%num2
        case '//':
            return num1//num2
    
def calc3(num1, num2, op):
    oper_dict = {
        '+' : num1 + num2,
        '-' : num1 - num2,
        '*' : num1 * num2,
        '/' : num1 / num2,
        '%' : num1 % num2,
        '//' : num1 // num2
    }
    return oper_dict[op]

def calc4(num1, num2, op):
    return eval(str(num1)+op+str(num2))

print(calc(20,2,'//'))
print(calc2(5,4,'*'))
print(calc4(1,2,'+'))