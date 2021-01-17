import random
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

'''Matte contains symbolic generation and solution of mathematical problems, such as: the chainrule, polynomial and exponential functions.
   Matte can integrate, derivate, simplify and expand functions.'''
class Matte():
    def __init__(self, my_math,p_max,n_st,my_sign):
        #inputs
        #Creates the symbol 'x' for symbolic analysis in sympy
        x = Symbol('x')
        #my_math is the math problem type to be solved
        self.my_math = my_math
        #Highest polynomial order
        self.p_max = p_max
        #Number of terms in the expression
        self.n_st = n_st
        #Allow positive or positive and negative signs
        self.my_sign = my_sign
        #outputs
        #The problem text that is parsed by sympy
        self.p_txt = ''
        #Highest order
        self.n = 0
        #Help text suitable for the problem type
        self.edu_txt = ''
        #Copy paste symbols suitable for the problem type
        self.pyperclip_txt = ''
        #The problem to be solved
        self.y = ''
        #The problem diffrentiated or simplified (chain rule only)
        self.y_diff = ''
        #The problem integrated or expanded (chain rule only)
        self.y_integrate = ''

    '''Generates polynomials of the type y = x => y'' = x^(n-1), e.g. y = 5*x^3 => y'' = 5*3*x^2'''
    def hel_polynom(self):
        #educational mode text
        self.edu_txt = 'y = x => y'' = x^(n-1), e.g. y = 5*x^3 => y'' = 5*3*x^2'
        # Store convenient text in Clipboard
        self.pyperclip_txt = '*x**'
        # Random integer between 1 and n_st+1
        self.n = random.randint(0, self.n_st - 1) + 2
        # print(self.n)
        for i in range(0, self.n):
            px = random.randint(0, self.p_max) + 1
            # create the text for sympy
            if self.my_sign == False:
                self.p_txt = self.p_txt + ' ' + str(px) + '*x**' + str(i)
            if self.my_sign == True:
                self.p_txt = self.p_txt + ' ' + str(random.choice((-1, 1))) + '*' + str(px) + '*x**(' + str(
                    random.choice((-1, 1))) + '*' + str(i) + ')'
            if i < self.n - 1:
                self.p_txt = self.p_txt + ' + '
        #
        # Create symbolic variable x for sympy
        x = Symbol('x')
        self.y = parse_expr(self.p_txt)
        #derivative
        self.y_diff = diff(self.y)
        #Integrate
        self.y_integrate = integrate(self.y)
        #
        return self.p_txt, self.n, self.edu_txt, self.pyperclip_txt,  self.y, self.y_diff, self.y_integrate

    '''Chain rule of the type (a-b)*(c+d) = a*c + a*d - b*c - b*d'''
    def kedjeregeln(self):
        #educational mode text
        self.edu_txt = '(a-b)*(c+d) = a*c + a*d - b*c - b*d'
        # Store convenient text in Clipboard
        self.pyperclip_txt = '*'
        # Random integer between 1 and n_st+1
        self.n = random.randint(0, self.n_st - 1) + 1
        if self.n == 0:
            self.n = 2
        # print(self.n)
        for i in range(0, self.n):
            px = random.randint(0, self.p_max)
            if px == 0:
                px = 1
            # create the text for sympy
            if self.my_sign == False:
                self.p_txt = self.p_txt + ' ' + '(' + str(px) + '+' + str(random.choice((-1, 1))) + '*' + str(px) + '*x**' + str(px) + ') *'
            if self.my_sign == True:
                self.p_txt = self.p_txt + ' '
            if i == self.n-1:
                self.p_txt = self.p_txt[:-1]
        #
        #print(self.p_txt)
        #y = parse_expr(self.p_txt)
        #print(y)
        x = Symbol('x')
        self.y = parse_expr(self.p_txt)
        # derivative
        #print(self.y)
        self.y_diff = self.y
        # Integrate
        self.y_integrate = expand(self.y)
        # sprint(y)
        return self.p_txt, self.n, self.edu_txt, self.pyperclip_txt,  self.y, self.y_diff, self.y_integrate
    '''Generates polynomials of the type y = x => y'' = x^(n-1), e.g. y = 5*x^3 => y'' = 5*3*x^2'''
    def halv_polynom(self):
        self.edu_txt = 'y = x => y'' = x^(n-1), e.g. y = 5*x^3 => y'' = 5*3*x^2'
        # Store convenient text in Clipboard
        self.pyperclip_txt = '*x**'
        # Random integer between 1 and n_st+2
        self.n = random.randint(0, self.n_st - 1) + 2
        # print(self.n)
        for i in range(1, self.n):
            px = random.randint(0, self.p_max)
            # create the text for sympy
            if self.my_sign == False:
                self.p_txt = self.p_txt + ' ' + str(px) + '*x**(1/' + str(i) + ')'
            if self.my_sign == True:
                self.p_txt = self.p_txt + ' ' + str(random.choice((-1, 1))) + '*' + str(px) + '*x**(' + str(
                    random.choice((-1, 1))) + '*1/' + str(i) + ')'
            if i < self.n - 1:
                self.p_txt = self.p_txt + ' + '
        #
        # print(p_txt)
        # skapa varaiabeln x
        x = Symbol('x')
        self.y = parse_expr(self.p_txt)
        #derivative
        self.y_diff = diff(self.y)
        #Integrate
        self.y_integrate = integrate(self.y)
        # sprint(y)
        return self.p_txt, self.n, self.edu_txt, self.pyperclip_txt,  self.y, self.y_diff, self.y_integrate

    '''Generates exponentials of the type y = x => y'' = x^(n-1), e.g. y = 5*x^3 => y'' = 5*3*x^2'''
    def e_exp(self):
        self.edu_txt = 'y = x => y'' = x^(n-1), e.g. y = 5*x^3 => y'' = 5*3*x^2'
        # Store convenient text in Clipboard
        self.pyperclip_txt = '*x**'
        #pyperclip.copy('*exp(x*')
        # Random integer between 1 and n_st+2
        self.n = random.randint(0, self.n_st - 1) + 2
        # print(n)
        for i in range(0, self.n):
            px = random.randint(0, self.p_max)
            # create the text for sympy
            if self.my_sign == False:
                self.p_txt = self.p_txt + ' ' + str(px) + '*exp(' + str(i) + '*x)'
            if self.my_sign == True:
                self.p_txt = self.p_txt + ' ' + str(random.choice((-1, 1))) + '*' + str(px) + '*exp(' + str(
                    random.choice((-1, 1))) + '*' + str(i) + '*x)'
            if i < self.n - 1:
                self.p_txt = self.p_txt + ' + '
        #
        # skapa varaiabeln x
        x = Symbol('x')
        self.y = parse_expr(self.p_txt)
        #derivative
        self.y_diff = diff(self.y)
        #Integrate
        self.y_integrate = integrate(self.y)
        # sprint(y)
        return self.p_txt, self.n, self.edu_txt, self.pyperclip_txt,  self.y, self.y_diff, self.y_integrate

    '''Generates exponentials of the type y = x => y'' = x^(n-1), e.g. y = 5*x^3 => y'' = 5*3*x^2'''
    def n_exp(self):
        self.edu_txt = 'y = x => y'' = x^(n-1), e.g. y = 5*x^3 => y'' = 5*3*x^2'
        # Store convenient text in Clipboard
        self.pyperclip_txt = '*x**'
        # STore convenient text in Clipboard
        #pyperclip.copy('*exp(x*')
        self.n = random.randint(0, self.n_st - 1) + 2
        # Random integer a
        a = random.randint(1, 11)
        # print(n)
        # Skapa polynomet med ordning n
        for i in range(0, self.n):
            px = random.randint(0, self.p_max)
            # create the text for sympy
            if self.my_sign == False:
                self.p_txt = self.p_txt + ' ' + str(px) + '*' + str(a) + '**(' + str(i) + '*x)'
            if self.my_sign == True:
                self.p_txt = self.p_txt + ' ' + str(random.choice((-1, 1))) + '*' + str(px) + '*' + str(a) + '**(' + str(
                    random.choice((-1, 1))) + '*' + str(i) + '*x)'
            if i < self.n - 1:
                self.p_txt = self.p_txt + ' + '
        #
        # skapa varaiabeln x
        x = Symbol('x')
        self.y = parse_expr(self.p_txt)
        #derivative
        self.y_diff = diff(self.y)
        #Integrate
        self.y_integrate = integrate(self.y)
        # 
        return self.p_txt, self.n, self.edu_txt, self.pyperclip_txt,  self.y, self.y_diff, self.y_integrate
