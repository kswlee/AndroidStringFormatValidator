import xml.etree.ElementTree as ET
import re


class Androidi18nStrings:
    def __init__(self, string_path, error_handler):
        self.error_handler = error_handler
        self.path = string_path
        self.white_list = []
        self.allowedDigits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.allowedControlChars = ['c', 'd', 'f', 's', '%']
        self.control_codes_map = {}
        self.string_map = {}
        self.read_xml()

    def read_xml(self):
        tree = ET.parse(self.path)
        root = tree.getroot()

        for stringElm in root:
            string_name = stringElm.attrib['name']
            strip_text = "".join(stringElm.itertext())
            code_map = self.validate_text(string_name, strip_text)
            self.control_codes_map[string_name] = code_map

    def match_ctrl_codes(self, lrs):
        for name in self.control_codes_map:
            cur_control_codes = self.get_control_codes_by_name(name)
            lrs_control_code = lrs.get_control_codes_by_name(name)

            cur_text = self.get_string_by_name(name).encode('utf-8')
            lrs_text = lrs.get_string_by_name(name).encode('utf-8')

            if len(lrs_control_code) > 0:
                for ctrl_code in lrs_control_code:
                    lrs_count = lrs_control_code[ctrl_code]
                    if ctrl_code not in cur_control_codes:
                        error_msg = "Error found in {}\n\tOri: {}\n\tTrans: {}\n\tReason - '{}': format code {} not matched\n".format(self.path,
                                                                                                     lrs_text,
                                                                                                     cur_text,
                                                                                                     name,
                                                                                                     ctrl_code)
                        self.on_error(name, error_msg)
                    else:
                        cur_count = cur_control_codes[ctrl_code]
                        if lrs_count != cur_count:
                            error_msg =  "Error found in {}\nOri: {}\nTrans: {}\nReason - '{}': format code {} not matched\n".format(self.path,
                                                                                                         lrs_text,
                                                                                                         cur_text,
                                                                                                         name,
                                                                                                         ctrl_code)
                            self.on_error(name, error_msg)

    def get_control_codes_by_name(self, name):
        return self.control_codes_map[name]

    def get_string_by_name(self, name):
        return self.string_map[name]

    def on_error(self, name, error):
        if name in self.white_list:
            self.error_handler(None, error)
            return

        self.error_handler(error, None)

    def validate_text(self, name, text):
        self.string_map[name] = text
        chars = [char for char in text]
        control_codes = []
        codes_counter = {}
        prev_char = ' '
        index = 0

        while index < len(chars):
            cur_char = chars[index]

            if prev_char == '%':
                if cur_char in self.allowedControlChars:
                    candidate = "{}{}".format(prev_char, cur_char)
                    if candidate == '%%':
                        index + index + 1
                        prev_char = ''
                        continue

                    control_codes.append(candidate)
                    if candidate in codes_counter:
                        codes_counter[candidate] = codes_counter[candidate] + 1
                    else:
                        codes_counter[candidate] = 1
                    pass
                elif cur_char in self.allowedDigits:
                    candidate = text[index-1:index+3]
                    prog = re.compile("\%\d\$s")
                    match = prog.match(candidate)
                    if match:
                        if candidate in codes_counter:
                            codes_counter[candidate] = codes_counter[candidate] + 1
                        else:
                            codes_counter[candidate] = 1
                        control_codes.append(candidate)

                    prev_char = ''
                    index = index + 3
                    continue
                    pass
                elif cur_char in ['0']:
                    candidate = text[index - 1:index + 3]
                    prog = re.compile("\%0\d\d")
                    match = prog.match(candidate)
                    if match:
                        if candidate in codes_counter:
                            codes_counter[candidate] = codes_counter[candidate] + 1
                        else:
                            codes_counter[candidate] = 1
                        control_codes.append(candidate)

                    prev_char = ''
                    index = index + 3
                    continue
                    pass
                else:
                    if name in self.white_list:
                        prev_char = ''
                        index = index + 1
                        continue
                    error_msg = "!!!! ERROR !!!! \nFile: {} \nInvalid format code detected: {} {}{}".format(self.path, name,
                                                                                               prev_char, cur_char)
                    self.on_error(name, error_msg)
                    prev_char = ''
                    continue

            prev_char = cur_char
            index = index + 1

        return codes_counter
