#Import necessary functions
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.togglebutton import ToggleButton, ToggleButtonBehavior
from kivy.uix.textinput import TextInput
from functools import partial
from kivy.graphics import Color, Rectangle
from kivy.utils import hex_colormap
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.lang import Builder
from random import random
from matte import Matte
from sympy.parsing.sympy_parser import parse_expr
from kivy.core.clipboard import Clipboard
import json
from kivy.properties import StringProperty, NumericProperty, OptionProperty, ObjectProperty, BooleanProperty
import requests
#
'''Language options that are controlled by the lang(language) switch,eg "En", "Sv".'''
mth_oper_options = {'expand_simplify': {'Sv': {'opt': ['Expandera', 'Förenkla']}, \
                              'En': {'opt': ['Expand', 'Simplify']}}, \
        'derive_integrate':{'Sv': {'opt': ['Derivera', 'Integrera']}, \
                          'En': {'opt': ['Derive', 'Integrate']}}}

mth_type_list = {'Sv':('Kedjeregeln','PolynomHel','PolynomHalv','ExponentialE', 'Exponentialn'),\
                'En':('Chainrule', 'PolynomWhole','PolynomHalf','ExponentWhole', 'ExponentHalf')}
mth_exp_val = ('1','2','3','4','5')

mth_paste_hints_txt = {'Sv':'Klistra in: ', 'En':'Paste: '}

mth_input_hints_txt = {'Sv':'Skriv ditt svar här + Enter när Du är klar', 'En':'Type in your answer here + Hit Enter'}

mth_edu_hints_txt = {'Sv':'Hjälptext', 'En':'Help Text'}
#
#To simplify debugging
def debug_print(txt):
    #below remove hash for debugging 
    #print(txt)
    pass
""""Inherit Image class properties to the Button class"""
class ImageButton(ButtonBehavior, Image):
    pass

"""The main class that create the GUI and control execution. """
class AntonsMatteApp(App):
    #
    number = NumericProperty(0)
    #
    """"The main function that creates the GUI"""
    def build(self):
        #
        debug_print('I build')
        #
        #The below is implemented as bug avoidance as the Matte app sometime produce 
        #cases that do not have answers. The while loop tests the case before releasing it and
        #simply makes a new case if a faulty one is produced.
        while True:
            try:
                self.tmp_math = Matte(my_math='n_exp', my_sign=False, p_max=2, n_st=5)
                self.tmp_math.n_exp()
                Clipboard.copy(self.tmp_math.pyperclip_txt)
                print('Y: ' + str(self.tmp_math.y))
                print('Ydiff: ' + str(self.tmp_math.y_diff))
                print('Yint: ' + str(self.tmp_math.y_integrate))
                if str(self.tmp_math.y_diff) != str() and str(self.tmp_math.y_integrate) != str():
                    break
            except:
                pass
        #
        """The i_change_screen funxtion switches to the screen named tmp_name"""
        def i_change_screen(tmp_name, instance):
            sm.current = str(tmp_name)
            if tmp_name is 'Home':
                sm.transition.direction ='right'
            else:
                sm.transition.direction = 'left'
        #
        """i_do_canvas creates the background wallpaper, ie the canvas. The Color RGB value controls the background color"""
        def i_do_canvas(my_wid, instance):
            with my_wid.canvas:
                Color(.38, .48, .55)
                Rectangle(pos=my_wid.pos, size=(2000,2000))
            wid = my_wid
        #
        """i_update_text is used to bind variables to kivy objects. This is a effective way to always uppdate graphical object variables."""
        def i_update_text(a_gui_var, instance, self):
            debug_print('u: '+a_gui_var)
            debug_print('u: '+str(instance))
            output = eval('instance.'+a_gui_var)
            return output
        #
        """special case to trigger update of mth_text"""
        def i_update_text2(a_gui_var, instance, self):
            debug_print('u: '+a_gui_var)
            debug_print('u: '+str(instance))
            my_gui_obj['Calculus'][1].text = str()
            return instance.text
        #
        """The clock loop is central to kivy and is neccessary to update GUI variables."""
        def i_do_clock(my_gui_obj, self, dt):
            #
            number = self.number
            #tmp_lang is introduced for convience
            tmp_lang = my_gui_obj['Calculus'][9].text
            """We only update the hint_text when language is switched."""
            if my_gui_obj['Calculus'][3].hint_text != str(mth_input_hints_txt[tmp_lang]):
                my_gui_obj['Calculus'][3].hint_text = str(mth_input_hints_txt[tmp_lang])
            my_gui_obj['Calculus'][14].text = str(mth_edu_hints_txt[tmp_lang])
            tmp_txt = my_gui_obj['Calculus'][11].text
            tmp_value = my_gui_obj['Calculus'][11].values
            tmp_toggle1 = my_gui_obj['Calculus'][7].text
            tmp_toggle2 = my_gui_obj['Calculus'][8].text
            toggle_gui_type = 'expand_simplify'
            #
            """Logic used to switch language"""
            if tmp_txt is 'Kedjeregeln' or tmp_txt is 'Chainrule':
                tmp_txt = mth_type_list[tmp_lang][0]
                tmp_value = mth_type_list[tmp_lang]
                my_math = mth_type_list['Sv'][0]
                toggle_gui_type = 'expand_simplify'
            if tmp_txt is 'PolynomHel' or tmp_txt is 'PolynomWhole':
                tmp_txt = mth_type_list[tmp_lang][1]
                my_math = mth_type_list['Sv'][1]
                toggle_gui_type = 'derive_integrate'
            if tmp_txt is 'PolynomHalv' or tmp_txt is 'PolynomHalf':
                tmp_txt = mth_type_list[tmp_lang][2]
                my_math = mth_type_list['Sv'][2]
                toggle_gui_type = 'derive_integrate'
            if tmp_txt is 'ExponentialE' or tmp_txt is 'ExponentWhole':
                tmp_txt = mth_type_list[tmp_lang][3]
                my_math = mth_type_list['Sv'][3]
                toggle_gui_type = 'derive_integrate'
            if tmp_txt is 'Exponentialn' or tmp_txt is 'ExponentHalf':
                tmp_txt = mth_type_list[tmp_lang][4]
                my_math = mth_type_list['Sv'][4]
                toggle_gui_type = 'derive_integrate'
            #
            my_gui_obj['Calculus'][7].text = mth_oper_options[toggle_gui_type][tmp_lang]['opt'][0]
            my_gui_obj['Calculus'][8].text = mth_oper_options[toggle_gui_type][tmp_lang]['opt'][1]
            #
            """This is where we create the mathematical task to be solved"""
            if my_gui_obj['Calculus'][1].text is str():
                n_st= int(my_gui_obj['Calculus'][10].text)
                while 0 is 0:
                    try:
                        p_max = round(random() * 29 + 1)
                        self.tmp_math = Matte(my_math=my_math, my_sign=False, p_max=p_max, n_st=n_st)
                        if my_math is 'Kedjeregeln':
                            self.tmp_math.kedjeregeln()
                        if my_math is 'PolynomHel':
                            self.tmp_math.hel_polynom()
                        if my_math is 'PolynomHalv':
                            self.tmp_math.halv_polynom()
                        if my_math is 'ExponentialE':
                            self.tmp_math.e_exp()
                        if my_math is 'Exponentialn':
                            self.tmp_math.n_exp()
                        Clipboard.copy(self.tmp_math.pyperclip_txt)
                        my_gui_obj['Calculus'][5].text = str(mth_paste_hints_txt[tmp_lang] + Clipboard.paste())
                        print(self.tmp_math.p_txt)
                        print(self.tmp_math.y)
                        print(self.tmp_math.y_diff)
                        print(self.tmp_math.y_integrate)
                        if str(self.tmp_math.y_diff) != str() or str(self.tmp_math.y_integrate) != str():
                            break
                        else:
                            print('Error')
                            print(p_max)
                            print(n_st)
                            print(my_math)
                            print(self.tmp_math.y)
                            print(self.tmp_math.y_diff)
                            print(self.tmp_math.y_integrate)

                    except:
                        debug_print('dummy save')
            #
            """Create math problem text"""
            if my_gui_obj['Calculus'][7].state is 'down':
                my_gui_obj['Calculus'][1].text = my_gui_obj['Calculus'][7].text + ': ' + str(self.tmp_math.y)
            if my_gui_obj['Calculus'][8].state is 'down':
                my_gui_obj['Calculus'][1].text = my_gui_obj['Calculus'][8].text + ': ' + str(self.tmp_math.y)
            #
            """Create help text"""
            if my_gui_obj['Calculus'][14].state is 'normal':
                my_gui_obj['Calculus'][2].text = str(self.tmp_math.edu_txt)
            if my_gui_obj['Calculus'][14].state is 'down':
                my_gui_obj['Calculus'][2].text = str()
            #
            #Update problem type and type list
            my_gui_obj['Calculus'][11].text = tmp_txt
            my_gui_obj['Calculus'][11].values = tmp_value
            #
            try:
                self.tmp_math
            except:
                self.tmp_math = ''
        #
        """The answer is compared with the correct answer here."""
        def i_check_answer(my_gui_obj, self, instance):
            #
            tmp_math = self.tmp_math
            #
            if my_gui_obj['Calculus'][7].state is 'down':
                correct_answer = str(tmp_math.y_integrate)
            if my_gui_obj['Calculus'][8].state is 'down':
                correct_answer = str(tmp_math.y_diff)
            #
            my_lang = my_gui_obj['Calculus'][9].text
            my_answer = {'Sv': ['Rätt Svar!', 'Fel - Korrekt svar är '], \
                         'En': ['Correct Answer!', 'Wrong - The right answer is ']}
            #
            if correct_answer is my_gui_obj['Calculus'][3].text:
                my_gui_obj['Calculus'][12].text = str(my_answer[my_lang][0])
                self.number += 1
                my_gui_obj['Calculus'][3].text = ''
                my_gui_obj['Calculus'][1].text = str()
            else:
                my_gui_obj['Calculus'][12].text = str(my_answer[my_lang][1] + correct_answer)
                self.number += 1
            #
            my_gui_obj['Calculus'][4].text = str(self.number)
            my_gui_obj['Calculus'][3].text = ''
            my_gui_obj['Calculus'][1].text = str()
            debug_print(self.number)
            debug_print('i_check_answer')
            debug_print('A: '+my_gui_obj['Calculus'][12].text)
            debug_print('B: ' + correct_answer)
            debug_print('C: ' + my_gui_obj['Calculus'][3].text)
        #
        self.my_lang = 'Sv'
        self.toggle_gui_type = 'expand_simplify'
        self.opt_gui_type = mth_type_list[self.my_lang][0]
        self.sel_exp = 2
        #
        #Parent for the kivy GUI
        sm = ScreenManager()
        scr_size_x = 600
        scr_size_y = 400
        i_define = dict()
        layout_list = ['GridLayout', 'FloatLayout']
        #
        """Story as a nested dict for configuring and creating the UI as kivy expressions""" 
        #page 1 
        story = {'Home': {0: {'gui_type': 'FloatLayout', 'size': '(scr_size_x, scr_size_y)'}, \
                          1: {'gui_type': 'Image', 'source': '"man.png"', 'pos_hint': '{"top": .98, "left": 1}',
                              'size_hint': '(1, .17)'}, \
                          2: {'gui_type': 'TextInput', 'hint_text': '"email"', 'size_hint': '(.8, .1)',
                              'pos_hint': '{"top": .75, "right": .9}'}, \
                          3: {'gui_type': 'TextInput', 'hint_text': '"password"', 'password': 'True',
                              'size_hint': '(.8, .1)',
                              'pos_hint': '{"top": .55, "right": .9}', 'text': 'str()'}, \
                          4: {'gui_type': 'Button', 'text': '"Sign Up!"', 'markup': 'True',
                              'size_hint': '(.8, .1)', 'pos_hint': '{"top": .2, "right": .9}'}, \
                          5: {'gui_type': 'ImageButton', 'source': '"pilbak4.png"',
                              'on_press': 'partial(i_change_screen,"Calculus")',
                              'size_hint': '(.1, .05)', 'pos_hint': '{"top": .4, "right": .98}'}}, \
                 'Calculus': {0: {'gui_type': 'FloatLayout', 'size': '(scr_size_x, scr_size_y)'}, \
                              1: {'gui_type': 'Label', 'text': 'str()', 'pos_hint': '{"top": .7, "right": .9}',
                                  'size_hint': '(.8, .1)', 'font_size': '16', 'bold': 'True'}, \
                              2: {'gui_type': 'Label', 'text': 'str()', 'pos_hint': '{"top": .78, "right": .9}',
                                  'size_hint': '(.8, .1)'}, \
                              3: {'gui_type': 'TextInput', 'hint_text': 'str(mth_input_hints_txt[self.my_lang])',
                                  'size_hint': '(.8, .1)', 'multiline': 'False', \
                                  'pos_hint': '{"top": .5, "right": .9}', 'text': 'str()',
                                  'on_text_validate': 'partial(i_check_answer, my_gui_obj, self)'}, \
                              4: {'gui_type': 'Label', 'text': 'str()', 'size_hint': '(.8, .1)',
                                  'pos_hint': '{"top": .42, "right": .457}'}, \
                              5: {'gui_type': 'Label',
                                  'text': 'str(mth_paste_hints_txt[self.my_lang] + Clipboard.paste())',
                                  'size_hint': '(.8, .5)',
                                  'pos_hint': '{"top": .77, "right": .55}', 'bold': 'True', 'color': '(0,0,0)'}, \
                              6: {'gui_type': 'ImageButton', 'source': '"pilbak3.png"',
                                  'on_press': 'partial(i_change_screen,"Home")', 'size_hint': '(.06, .05)',
                                  'pos_hint': '{"center": (.04, .95)}'}, \
                              7: {'gui_type': 'ToggleButton',
                                  'text': 'str(mth_oper_options[self.toggle_gui_type][self.my_lang]["opt"][0])', \
                                  'size_hint': '(.1, .08)', 'pos_hint': '{"center": (.76, .95)}', 'group': '"tb"',
                                  'state': '"down"'}, \
                              8: {'gui_type': 'ToggleButton',
                                  'text': 'str(mth_oper_options[self.toggle_gui_type][self.my_lang]["opt"][1])',
                                  'size_hint': '(.1, .08)',
                                  'pos_hint': '{"center": (.86, .95)}', 'group': '"tb"', 'state': '"normal"'}, \
                              9: {'gui_type': 'Spinner', 'text': 'self.my_lang', 'size_hint': '(.1, .09)',
                                  'pos_hint': '{"top": .75, "right": .1}', 'values': '("Sv", "En")'}, \
                              10: {'gui_type': 'Spinner', 'text': 'str(self.sel_exp)', 'size_hint': '(.09, .08)',
                                   'pos_hint': '{"center": (.955, .95)}', \
                                   'values': 'mth_exp_val'}, \
                              11: {'gui_type': 'Spinner', 'size_hint': '(.15, .08)',
                                   'pos_hint': '{"center": (.6333, .95)}',
                                   'text': 'self.opt_gui_type', 'values': 'mth_type_list[self.my_lang]'}, \
                              12: {'gui_type': 'Label', 'text': 'str()', 'pos_hint': '{"top": .38, "right": .9}',
                                   'size_hint': '(.8, .1)'}, \
                              13: {'gui_type': 'Label', 'text': '"# "', 'size_hint': '(.8, .1)',
                                   'pos_hint': '{"top": .42, "right": .47}', 'halign': '"left"',
                                   'valign': '"middle"'}, \
                              14: {'gui_type': 'ToggleButton', 'text': '"Hjälptext"',
                                   'pos_hint': '{"top": .85, "right": .1}', 'size_hint': '(.1, .09)',
                                   'state': '"normal"'}}}
        #
        my_gui_obj = dict()
        #
        """These for-loops read the variable "story" and interpret the kivy commands.
           The parent child structure is that sm (ScreenManager) is the parent, scr(Screen) are children.
           In each screen is a layout of which widgets are it's children."""
        for a_screen_name in story:
            scr = Screen(name=str(a_screen_name))
            my_gui_obj[a_screen_name] = dict()
            for idx in story[a_screen_name]:
                gui_story_row = story[a_screen_name][idx]
                txt = str()
                for gui_variable in gui_story_row:
                    if gui_variable == 'gui_type':
                        gui_type = gui_story_row['gui_type']
                        txt = txt + gui_type +'('
                    if gui_variable != 'gui_type':
                        value = str(gui_story_row[gui_variable])
                        txt = txt + gui_variable +' = '+value+', '
                #
                txt = txt + ')'
                #
                if gui_type in layout_list:
                    """Eval interpret txt which is the kivy command from story"""
                    gl = eval(txt)
                    if gui_type is 'FloatLayout':
                        my_gui_obj[a_screen_name][idx] = Widget()
                        gl.add_widget(my_gui_obj[a_screen_name][idx], canvas='before')
                        Clock.schedule_once(partial(i_do_canvas,my_gui_obj[a_screen_name][idx]))
                    if gui_type is 'FloatLayout':
                        btn = Widget()
                        my_gui_obj[a_screen_name][idx] = gl.add_widget(btn)
                else:
                    debug_print(txt)
                    my_gui_obj[a_screen_name][idx] = eval(txt)
                    try:
                        my_var_list = list(my_gui_obj[a_screen_name][idx]._kwargs_applied_init)
                        debug_print(my_var_list)
                        for a_gui_var in my_var_list:
                            try:
                                if a_gui_var is 'text' and a_screen_name is 'Calculus' and idx in [7,8,9,10,11]:
                                    debug_print(a_gui_var + a_screen_name + str(idx))
                                    # Special case to generate new equation
                                    my_gui_obj[a_screen_name][idx].bind(text=partial(i_update_text2, a_gui_var))
                                else:
                                    debug_print(a_gui_var)
                                    #makes sure all initiated vars are updated in dict
                                    debug_print('my_gui_obj[a_screen_name][idx].bind(' + str(a_gui_var) + '=partial(i_update_text,"'+a_gui_var+'")')
                                    eval('my_gui_obj[a_screen_name][idx].bind(' + str(a_gui_var) + '=partial(i_update_text,str('+a_gui_var+'))')
                            except:
                                pass
                    except:
                       pass
                    #add layout and widget to the layout
                    gl.add_widget(my_gui_obj[a_screen_name][idx])
            #add layout and children to the screen
            scr.add_widget(gl)
            #Add screen to the screenmanager
            sm.add_widget(scr)
            #Execute clock cycle every .2 second by executing the i_do_clock function.
            #partial is used to pass the variables my_gui_obj and self to the i_do_clock function.
            Clock.schedule_interval(partial(i_do_clock, my_gui_obj, self), .2)
        return sm

"""Run program"""
if __name__ == '__main__':
    AntonsMatteApp().run()

