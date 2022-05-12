def binAddCarry(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)

    result = ''
    carry = 0
    flag = False

    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if a[i] == '1' else 0
        r += 1 if b[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result

        carry = 0 if r < 2 else 1
    if carry != 0:
        flag = True

        #the number will be a positive number and the carry bit will be discarded and remaining bits are the final result.
        return [result.zfill(max_len), flag]
    else:

        #we take the 2's complement of the result to get the final result.
        return [result.zfill(max_len), flag]


def shift(num, diff, digits):
    temp = "1" + num[2]
    temp = int(temp, 2) >> diff
    temp = toBinary(temp)
    temp = str('0' * (digits - len(str(temp)))) + temp
    return (temp)


def toBinary(num):
    return bin(int(num))[2:]


def twoComplement(num):
    inverse = ''.join(['1' if i == '0' else '0' for i in num])
    sum = str(bin(int(inverse, 2) + int("1", 2))[2:])
    sum = (len(num) - len(sum)) * "0" + sum
    return sum


def fracToBin(n):
    binary = str()

    while (n):
        n *= 2

        if (n >= 1):
            int_part = 1
            n -= 1
        else:
            int_part = 0

        binary += str(int_part)
    return binary


def intTo32bin(n):
    sign_bit = 0

    if (n < 0):
        sign_bit = 1

    n = abs(n)

    int_str = bin(int(n))[2:32]

    fraction_str = fracToBin(n - int(n))

    if (n == 0):
        return ['0', '00000000', '00000000000000000000000']
    else:
        index = int_str.index('1')
        exponent = bin((len(int_str) - index - 1) + 127)[2:]
        exponent = '0' * (8 - len(exponent)) + exponent
        mantissa = int_str[index + 1:23] + fraction_str
        mantissa = mantissa + ('0' * (23 - len(mantissa)))
        if (len(mantissa) > 23):
            mantissa = bin(int(mantissa[0:23], 2) + 1)[2:]
            mantissa = '0' * (23 - len(mantissa)) + mantissa
        return [sign_bit, exponent, mantissa]


def binAdd(num1, num2):
    num1, num2 = intTo32bin(num1), intTo32bin(num2)
    temp1 = ''
    temp2 = ''
    mantissa = ''
    flag = 0
    print("\t" + str(num1[0]) + " " + num1[1] + " " + num1[2] + "\n+\t" +
          str(num2[0]) + " " + num2[1] + " " + num2[2])
    print("=" * 42)

    #if the exponents are different
    if (num1[1] != num2[1]):
        diff = abs(int(num1[1], 2) - int(num2[1], 2))
        #num 1 is bigger flag 0
        if (int(num1[1], 2) > int(num2[1], 2)):
            temp2 = shift(num2, diff, 24)
            temp1 = '1' + num1[2]

        #num 2 is bigger flag 1
        else:
            temp1 = shift(num1, diff, 24)
            temp2 = '1' + num2[2]
            flag = 1
    else:
        temp1 = '1' + num1[2]
        temp2 = '1' + num2[2]

    #if both numbers are positive
    if (num1[0] == 0 and num2[0] == 0):
        if (flag == 0):
            mantissa = str(bin(int(temp1, 2) + int(temp2, 2))[3:26])
            return [num1[0], num1[1], mantissa]
        else:
            mantissa = str(bin(int(temp1, 2) + int(temp2, 2))[3:26])
            return [num2[0], num2[1], mantissa]

    #if both numbers are negative
    if (num1[0] == 1 and num2[0] == 1):
        if (flag == 0):
            mantissa = str(bin(int(temp1, 2) + int(temp2, 2))[3:])
            return [num1[0], num1[1], mantissa]
        else:
            mantissa = str(bin(int(temp1, 2) + int(temp2, 2))[3:])
            return [num2[0], num2[1], mantissa]

    #if one of them are negative
    else:
        temp2 = twoComplement(temp2)
        sum = binAddCarry(temp1, temp2)
        if sum[1] == True:
            mantissa = sum[0][1:]
            return [num1[0], num1[1], mantissa]
        elif sum[1] == False:
            mantissa = twoComplement(sum[0])[1:]
            return [num1[0], num1[1], mantissa]


def binMul(num1, num2):
    if (num1 == 0 or num2 == 0):
        return intTo32bin(0.0)
    elif (num1 == 1):
        return intTo32bin(num2)
    elif (num2 == 1):
        return intTo32bin(num1)
    else:
        num1, num2 = intTo32bin(num1), intTo32bin(num2)
        print("\t" + str(num1[0]) + " " + num1[1] + " " + num1[2] + "\nX\t" +
              str(num2[0]) + " " + num2[1] + " " + num2[2])
        print("=" * 42)
        exp = bin(int(num1[1], 2) + int(num2[1], 2))[2:]
        num1[2], num2[2] = '1' + num1[2], '1' + num2[2]
        mantissa = bin(int(num1[2], 2) * int(num2[2], 2))[3:25]
        index = mantissa.index('1')
        mantissa = mantissa + "0" * (23 - len(mantissa))
        if (index == 0):
            exp = bin(int(num1[1], 2) + int(num2[1], 2) - 127)[2:10]

        elif (index != 0):
            exp = bin(int(num1[1], 2) + int(num2[1], 2) - 127 +
                      int("1", 2))[2:10]
        signbit = num1[0] ^ num2[0]
        return [signbit, exp, mantissa]


def binDiv(num1, num2):
    if (num2 == 0):
        print("Inf Error")
    elif (num1 == 0):
        return intTo32bin(0.0)
    else:
        num1, num2 = intTo32bin(num1), intTo32bin(num2)
        print("\t" + str(num1[0]) + " " + num1[1] + " " + num1[2] + "\n/\t" +
              str(num2[0]) + " " + num2[1] + " " + num2[2])
        print("=" * 42)
        exponent = bin(int(num1[1], 2) - int(num2[1], 2) + 127)[2:]
        exponent = '0' * (8 - len(exponent)) + exponent
        temp1 = '1' + num1[2]
        temp2 = '1' + num2[2]
        mantissa = int(temp1, 2) / int(temp2, 2)
        mantissa = intTo32bin(mantissa)
        mantissa = mantissa[2]
        signbit = num1[0] ^ num2[0]
        return [signbit, exponent, mantissa]


def bin32toInt(bin):
    signbit = bin[0]
    exponent = int(bin[1], 2) - 127
    mantissa = bin[2]
    mantissa_int = 0
    power_count = -1

    for i in mantissa:
        mantissa_int += (int(i) * pow(2, power_count))
        power_count -= 1
    mantissa_int += 1
    number = pow(-1, signbit) * mantissa_int * pow(2, exponent)
    return number


if __name__ == "__main__":
    while(True):
        print("Enter two numbers: ")
        a = float(input("A= "))
        b = float(input("B= "))
        print(
            "Select an operation:\n\n1: Addition\n2: Subtraction\n3: Multiplication\n4: Division\n5: Change numbers"
        )
        inp = int(input("Enter choice: "))

        while (inp != 5):
            if (inp == 1):
                sum = binAdd(a, b)
                print("\t" + str(sum[0]) + " " + sum[1] + " " + sum[2])
                print("In decimal form : ", bin32toInt(sum))
            elif (inp == 2):
                sum = binAdd(a, -b)
                print("\t" + str(sum[0]) + " " + sum[1] + " " + sum[2])
                print("In decimal form : ", bin32toInt(sum))
            elif (inp == 3):
                product = binMul(a, b)
                print("\t" + str(product[0]) + " " + product[1] + " " + product[2])
                print("In decimal form : ", bin32toInt(product))
            elif (inp == 4):
                quotient = binDiv(a, b)
                if (b == 0):
                    pass
                else:
                    print("\t" + str(quotient[0]) + " " + quotient[1] + " " +
                        quotient[2])
                    print("In decimal form : ", bin32toInt(quotient))
            print(
                "Select an operation:\n\n1: Addition\n2: Subtraction\n3: Multiplication\n4: Division\n5: Change numbers"
            )
            inp = int(input("Enter choice: "))
