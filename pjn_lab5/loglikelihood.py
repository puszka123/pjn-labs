import math


def xLogX(x):
    if x == 0:
        return 0.0
    else:
        return x * math.log(x)


def entropy(*arg):
    sum = 0
    result = 0.0
    for element in arg:
        result += xLogX(element)
        sum += element

    return xLogX(sum) - result


def loglikelihoodRatio(k11, k12, k21, k22):
    rowEntropy = entropy(k11 + k12, k21 + k22)
    columnEntropy = entropy(k11 + k21, k12 + k22)
    matrixEntropy = entropy(k11, k12, k21, k22)
    if rowEntropy + columnEntropy < matrixEntropy:
        return 0.0
    return 2.0 * (rowEntropy + columnEntropy - matrixEntropy)
