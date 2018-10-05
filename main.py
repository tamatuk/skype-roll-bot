def try_resolve_input(input_line):
    try:
        return resolve_input(input_line)
    except ValueError as e: 
        return str(e)

def resolve_input(input_line):
    expression, repetitions = unpack_input(input_line)
    result = []
    for i in range(repetitions):
        result.append(resolve_expression(expression))
    return '\n'.join(result)

def unpack_input(input_line):
    input_array = input_line.split(' ')
    if not len(input_array):
        raise ValueError('Empty input')
    if len(input_array)>1:
        repetitions = check_repititions(input_array[1])
    else:
        repetitions = 1
    line = input_array[0]
    return line, repetitions

def check_repititions(s):
    i = try_resolve_repetitions(s)
    if i>0:
        return i
    else:
        raise ValueError('Number of repetitions(' + s + ') should be positive')

def try_resolve_repetitions(s):
    try:
        return int(s)
    except ValueError:
        raise ValueError('Number of repetitions(' + s + ') should be integer')

def resolve_expression(expression):
    input_signs, input_elements = split_signs_and_elements(expression)
    result_string, result_value = resolve_element(input_elements[0])
    for i, sign in enumerate(input_signs):
        element = input_elements[i+1]
        string, value = resolve_element(element)
        result_string += sign + string
        result_value = apply_sign_to_values(result_value, value, sign)
    return result_string + '=' +str(result_value)

def split_signs_and_elements(line):
    delimetersRe = '\+|\-'
    import re
    signs = re.findall(delimetersRe, line)
    elements = re.split(delimetersRe, line)
    return signs, elements

def apply_sign_to_values(value1, value2, sign):
    if sign == '+':
        return value1+value2
    elif sign == '-':
        return value1-value2
    else:
        raise ValueError('Unrecognized sing "' + sign + '"')

def resolve_element(input_element):
    import re
    if re.fullmatch(r'([1-9][0-9]*d[1-9][0-9]*(d[1-9][0-9]*)?)', input_element):
        return resolve_dice(input_element)
    if re.fullmatch(r'[1-9][0-9]*', input_element):
        return resolve_flat_number(input_element)
    else:
        raise ValueError('Unrecognized element "' + input_element + '"')
        
def resolve_dice(dice_string):
    dice_count, dice_value, dice_drop = unpack_dice(dice_string)
    if dice_drop >= dice_count:
        raise ValueError('Dropped more or equal then rolled in dice "' + dice_string + '"')
    from random import randint 
    dice_rolls = [randint(1, dice_value) for r in range(dice_count)]
    result_strings = []
    result_value = 0
    import heapq
    droped_dices = heapq.nsmallest(dice_drop, dice_rolls)
    for value in dice_rolls:
        if value in droped_dices:
            result_strings.append(strike(str(value)))
            droped_dices.remove(value)
        else:
            result_strings.append(str(value))
            result_value += value
    return '+'.join(result_strings), result_value

def unpack_dice(dice_string):
    dice_array = dice_string.split('d')
    if len(dice_array) > 2:
        dice_drop = int(dice_array[2])
    else:
        dice_drop = 0
    dice_count = int(dice_array[0])
    dice_value = int(dice_array[1])  
    return dice_count, dice_value, dice_drop
    
def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

def resolve_flat_number(input_element):
    return input_element, int(input_element)

import logging
from settings import skype_login, skype_password

from skpy import SkypeEventLoop, SkypeNewMessageEvent
class Skype(SkypeEventLoop):
    def __init__(self):
        super(Skype, self).__init__(skype_login, skype_password)
    def onEvent(self, event):
        logging.debug(repr(event), exc_info=True)
        if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId:
            if event.msg.content[:3] == '/r ' or event.msg.content[:3] == '!r ':
                event.msg.chat.sendMsg(try_resolve_input(event.msg.content[3:]))

def create_server():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='log.txt',level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S')
    while True:
        try:
            sk = Skype()
            sk.loop()
        except:
            logging.error("Fatal error in main loop", exc_info=True)

if __name__ == "__main__":
	create_server()

