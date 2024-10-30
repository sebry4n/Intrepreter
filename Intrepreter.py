
class TokenType:
    MAKE = "MAKE"
    ASSIGN_TYPE = "ASSIGN_TYPE"
    ASSIGN_VALUE = "ASSIGN_VALUE"
    CONVERT = "CONVERT"
    PRINT = "PRINT"
    IDENTIFIER = "IDENTIFIER"
    VALUE = "VALUE"

def lexer(line):
    tokens = []
    words = line.split()
    if words[0] == "BUAT":
        tokens.append((TokenType.MAKE, words[1]))
    elif len(words) > 2 and words[1] == "ITU":
        tokens.append((TokenType.ASSIGN_TYPE, words[0], words[2]))
    elif len(words) > 2 and words[1] == "NILAI":
        tokens.append((TokenType.ASSIGN_VALUE, words[0], words[2]))
    elif len(words) > 2 and words[1] == "JADI":
        tokens.append((TokenType.CONVERT, words[0], words[2]))
    elif words[0] == "PLAK":
        tokens.append((TokenType.PRINT, words[1]))
    return tokens


class Interpreter:
    def __init__(self):
        self.variables = {}

    def process_line(self, line):
        tokens = lexer(line)
        for token in tokens:
            token_type = token[0]
            if token_type == TokenType.MAKE:
                _, var_name = token
                self.variables[var_name] = {"type": None, "value": None, "display_value": None, "original_value": None}
            elif token_type == TokenType.ASSIGN_TYPE:
                _, var_name, var_type = token
                if var_name in self.variables:
                    self.variables[var_name]["type"] = var_type
            elif token_type == TokenType.ASSIGN_VALUE:
                _, var_name, value_str = token
                if var_name in self.variables and self.variables[var_name]["type"] is not None:
                    var_type = self.variables[var_name]["type"]
                    value, display_value = self.parse_value(value_str, var_type)
                    self.variables[var_name]["value"] = value
                    self.variables[var_name]["display_value"] = display_value
                    self.variables[var_name]["original_value"] = value
            elif token_type == TokenType.CONVERT:
                _, var_name, to_format = token
                if var_name in self.variables and self.variables[var_name]["value"] is not None:
                    self.convert(var_name, to_format)
            elif token_type == TokenType.PRINT:
                _, var_name = token
                if var_name in self.variables:
                    print(self.variables[var_name]["display_value"])

    def parse_value(self, value_str, var_type):
        if var_type == "DECIMAL":
            return int(value_str), value_str
        elif var_type == "BINER":
            value = int(value_str, 2)
            return value, bin(value)[2:]  
        elif var_type == "OCTAL":
            value = int(value_str, 8)
            return value, oct(value)[2:] 
        elif var_type == "HEXA":
            value = int(value_str, 16)
            return value, value_str.upper()

    def convert(self, var_name, to_format):
        original_value = self.variables[var_name]["original_value"]
        if to_format == "BINER":
            self.variables[var_name]["display_value"] = bin(original_value)[2:]
        elif to_format == "OCTAL":
            self.variables[var_name]["display_value"] = oct(original_value)[2:]
        elif to_format == "HEXA":
            self.variables[var_name]["display_value"] = hex(original_value)[2:].upper()
        elif to_format == "DECIMAL":
            self.variables[var_name]["display_value"] = str(original_value)


def main(file_path):
    interpreter = Interpreter()
    
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                interpreter.process_line(line)

oll_file_path = "D:\Project\python\SturkDatNAlgo\input.oll"
main(oll_file_path)
