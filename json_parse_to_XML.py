from parglare import Parser, Grammar

grammar = r"""
json: element;
value: object | array | string | number | true | false | null;
object: '{' ws '}' | '{' member '}';
member: member ',' member {8} | EMPTY {9} | ws string ws ':' element;
array: '[' ws ']' | '[' element ']';
element: element ',' element {7} | EMPTY {9} | ws value ws;
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
true: 'true';
false: 'false';
null: 'null';
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

def add_tag(tag_name, content):
    tagged_content = ""
    return tagged_content

actions = {
    "json": lambda _, json: "<json>" + json[0] + "</json>",
    "value": [lambda _, value: "<value type=\"object\">" + value[0] + "</value>",
              lambda _, value: "<value type=\"array\">" + value[0] + "</value>",
              lambda _, value: "<value type=\"string\">" + value[0] + "</value>",
              lambda _, value: "<value type=\"number\">" + value[0] + "</value>",
              lambda _, value: "<value type=\"true\">" + value[0] + "</value>",
              lambda _, value: "<value type=\"false\">" + value[0] + "</value>",
              lambda _, value: "<value type=\"null\">" + value[0] + "</value>"],
    "object": [lambda _, obj: obj, 
               lambda _, obj: obj[1]],
    "member": [lambda _, member: member[0] + member[2],
               lambda _, member: member,
               lambda _, member: "<memberKey>" + member[1] + "</memberKey>" + "<member>" + member[4] + "</member>"],
    "array": [lambda _, array: array,
              lambda _, array: array[1]],
    "element": [lambda _, element: element[0] + element[2],
                lambda _, element: element[0],
                lambda _, element: element[1]],
    "string": lambda _, string: ''.join(string[1]),
    "character": [lambda _, char: char[0] + char[1],
                  lambda _, char: char,
                  lambda _, char: char,
                  lambda _, char: char,
                  lambda _, char: char],
    "number": lambda _, number: combine_number(number),
    "int": [lambda _, integer: ''.join(integer),
            lambda _, integer: "-" + integer],
    "digit": [lambda _, digit: digit[0] + digit[1],
              lambda _, digit: digit[0],
              lambda _, digit: digit[0],
              lambda _, digit: digit[0]]
} 


json = '{"colors": [{"color": "black", "category": "hue", "type": "primary", "code": {"rgba": [255, 255, 255, 1], "hex": "#000"}}, {"color": "white", "category": "value", "code": {"rgba": [0, 0, 0, 1], "hex": "#FFF"}}, {"color": "red", "category": "hue", "type": "primary", "code": {"rgba": [255, 0, 0, 1], "hex": "#FF0"}}, {"color": "blue", "category": "hue", "type": "primary", "code": {"rgba": [0, 0, 255, 1], "hex": "#00F"}}, {"color": "yellow", "category": "hue", "type": "primary", "code": {"rgba": [255, 255, 0, 1], "hex": "#FF0"}}, {"color": "green", "category": "hue", "type": true, "code": {"rgba": [0, 255, 0, 1], "hex": "#0F0"}}]}'

g = Grammar.from_string(grammar)

parser = Parser(g, debug=True, ws=None, actions=actions)

result = parser.parse(json)

def pretty_printer(raw_xml):
    xml_list = get_tokens(raw_xml)
    tab = "    "
    nl = "\n"
    t = -1
    c = 2
    for i in range(len(xml_list)):
        if len(xml_list[i]) > 1 and xml_list[i][1] == '/':
            c -= 1
            t -= 1
            xml_list[i] = nl + t*tab + xml_list[i]
        else:
            if c % 2 == 0:
                t += 1
                c += 1
            xml_list[i] = nl + t*tab + xml_list[i]
    return ''.join(xml_list)

def get_tokens(raw_xml):
    import re
    temp_list = re.findall('[^>]+>', raw_xml)
    xml_list = temp_list.copy()
    xml_items = []
    for i in range(len(temp_list)):
        if temp_list[i][0] == '<':
            continue
        else:
            item = re.findall('(?:(?!<).)*', temp_list[i])
            xml_list[i] = 'XXXX'
            xml_items.append(["<" + item[2], item[0]])
    while 'XXXX' in xml_list:
        i = xml_list.index('XXXX')
        items = xml_items.pop(0)
        xml_list[i] = items[0]
        xml_list.insert(i, items[1])
    return xml_list

print(pretty_printer(result))