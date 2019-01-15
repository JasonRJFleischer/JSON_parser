from parglare import Parser, Grammar

grammar = r"""
json: element;
value: object | array | string | number | 'true' | 'false' | 'null';
object: '{' ws '}' | '{' members '}';
members: member | member ',' members;
member: ws string ws ':' element;
array: '[' ws ']' | '[' elements ']';
elements: element | element ',' elements;
element: ws value ws;
string: '"' characters '"';
characters: EMPTY | character characters;
character: non_digit_hex | hex | reverse_solidus escape;
escape: escape_character | hex_escape_character hex hex hex hex;
hex: digit | hex_uppercase | hex_lowercase;
number: int frac exp;
int: digit | onenine digits | '-' digit | '-' onenine digits;
digits: digit | digit digits;
digit: '0' | onenine;
frac: EMPTY | dot digits;
exp: EMPTY | 'E' sign digits | 'e' sign digits;
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

json = '{"colors": [{"color": "black", "category": "hue","type": "primary","code": {"rgba": [255,255,255,1],"hex": "#000"}},{"color": "white","category": "value","code": {"rgba": [0,0,0,1],"hex": "#FFF"}},{"color": "red","category": "hue","type": "primary","code": {"rgba": [255,0,0,1],"hex": "#FF0"}},{"color": "blue","category": "hue","type": "primary","code": {"rgba": [0,0,255,1],"hex": "#00F"}},{"color": "yellow","category": "hue","type": "primary","code": {"rgba": [255,255,0,1],"hex": "#FF0" }}, {"color": "green","category": "hue","type": "secondary","code": {"rgba": [0,255,0,1],"hex": "#0F0"}}]}'

g = Grammar.from_string(grammar)

parser = Parser(g, debug=True, ws=None)

result = parser.parse(json)

print('Result:', result)