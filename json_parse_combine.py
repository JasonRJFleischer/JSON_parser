from parglare import Parser, Grammar

# define the grammar
grammar = r"""
json: element;
value: object | array | string | number | 'true' | 'false' | 'null';
object: '{' ws '}' | '{' member '}';
member: member ',' member {6} | EMPTY {7} | ws string ws ':' element;
array: '[' ws ']' | '[' element ']';
element: element ',' element {5} | EMPTY {8} | ws value ws;
string: '"' character '"';
character: character character | EMPTY | non_digit_hex | hex | reverse_solidus escape;
escape: escape_character | hex_escape_character hex hex hex hex;
hex: digit | hex_uppercase | hex_lowercase;
number: int frac exp;
int: digit | '-' digit;
digit: digit digit | EMPTY {9} | '0' | onenine;
frac: EMPTY | dot digit;
exp: EMPTY | 'E' sign digit | 'e' sign digit;
sign: EMPTY | '+' | '-';
ws: EMPTY | tab ws | lf ws | cr ws | sp ws;

terminals
tab: /[\u0009]/;
lf: /[\u000a]/;
cr: /[\u0009]/;
sp: /[\u0020]/;
non_digit_hex: /[\u0020-\u0021-\u0023-\u002F-\u003A-\u0040-\u0047-\u005B-\u005D-\u0060-\u0067-\uffff]/;
escape_character: /[\u0022, \u005C, \u002f, \u0062, \u0066, \u006E, \u0072, \u0074]/;
hex_escape_character: /[\u0075]/; 
reverse_solidus: /[\u005C]/;
onenine: /[1-9]/;
hex_uppercase: /[A-F]/;
hex_lowercase: /[a-f]/;
dot: /[.]/;
"""

# helper functions for actions
def debug_action(x):
    print(x)
    return x

def combine_number(number):
    combined_number = ''
    for i in range(len(number)):
        if number[i] != []:
            combined_number = combined_number + number[i]
    return combined_number 

# define the actions
actions = {
    "object": [lambda _, obj: obj, 
               lambda _, obj: obj[0] + obj[1] + obj[2]],
    "member": [lambda _, member: member[0] + member[1] + " " + member[2],
               lambda _, member: member,
               lambda _, member: member[1] + member[3] + " " + member[4]],
    "array": [lambda _, array: array,
              lambda _, array: array[0] + array[1] + array[2]],
    "element": [lambda _, element: element[0] + element[1] + " " + element[2],
                lambda _, element: element[0],
                lambda _, element: element[1]],
    "string": lambda _, string: string[0] + ''.join(string[1]) + string[2],
    "character": [lambda _, char: char[0] + char[1],
                  lambda _, char: char,
                  lambda _, char: char,
                  lambda _, char: char,
                  lambda _, char: char],
    "number": lambda _, number: debug_action(combine_number(number)),
    "int": [lambda _, integer: ''.join(integer),
            lambda _, integer: "-" + integer],
    "digit": [lambda _, digit: digit[0] + digit[1],
              lambda _, digit: digit[0],
              lambda _, digit: digit[0],
              lambda _, digit: digit[0]]
} 

# JSON to test on
json = '{"colors": [{"color": "black", "category": "hue", "type": "primary", "code": {"rgba": [255, 255, 255, 1], "hex": "#000"}}, {"color": "white", "category": "value", "code": {"rgba": [0, 0, 0, 1], "hex": "#FFF"}}, {"color": "red", "category": "hue", "type": "primary", "code": {"rgba": [255, 0, 0, 1], "hex": "#FF0"}}, {"color": "blue", "category": "hue", "type": "primary", "code": {"rgba": [0, 0, 255, 1], "hex": "#00F"}}, {"color": "yellow", "category": "hue", "type": "primary", "code": {"rgba": [255, 255, 0, 1], "hex": "#FF0"}}, {"color": "green", "category": "hue", "type": "secondary", "code": {"rgba": [0, 255, 0, 1], "hex": "#0F0"}}]}'

g = Grammar.from_string(grammar)

parser = Parser(g, debug=True, ws=None, actions=actions)

result = parser.parse(json)

print("Result = ", result, "\n\n" + "Result == JSON?", result == json)