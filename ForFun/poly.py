# -*- coding: utf-8 -*-

class Derivative:
    def __init__(self, polynomial=''):
        self.__polynomial = polynomial

    def input(self, polynomial=''):
        self.__polynomial = input('Input the polynomial:')

    def derivative(self):
        list1 = self.__polynomial.split('+')
        list4 = []

        for i in list1:

            try:
                float(i)
            except ValueError:

                list2 = i.split('*')
                if len(list2) == 1:  ## no coefficient
                    list3 = list2[0].split('^')
                    if len(list3) == 1:  ## x
                        result = '1'
                        list4.append(result)
                    else:  ## x^2
                        result = list3[1] + '*' + list3[0] + '^' + str(float(list3[1]) - 1)
                        list4.append(result)

                else:  ##with coefficient
                    list3 = list2[1].split('^')

                    if len(list3) == 1:  ## no exponential 5*x
                        result = list2[0]
                        list4.append(result)
                    else:  ## with exponential 2*x^3
                        coefficient = float(list2[0]) * float(list3[1])
                        term = list3[0]
                        exponential = float(list3[1]) - 1
                        result = str(coefficient) + '*' + term + '^' + str(exponential)
                        list4.append(result)

        answer = ''
        for k in list4:
            answer = answer + '+' + k
        answer = answer[1:]
        return answer


def main():
    d = Derivative('5*x^2-3*x')
    # d.input()
    print(d.derivative())


main()
