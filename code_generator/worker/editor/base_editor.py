import logging
import re

logger = logging.getLogger(__name__)

def format_line_for_save(s):
    s1 = re.sub('^[0-9]+', '', s)
    s2 = s1 + '\n' if len(s1) == 0 or s1[-1] != '\n' else s1

    return s2

def format_line_for_load(i, s):
    s1 = s + '\n' if s[-1] != '\n' else s
    s2 = re.sub('^[0-9]+', '', s1)
    s3 = '{} '.format(i + 1) + s2
    return s3

class BaseEditor:
    def __init__(self, source_file_path):
        logger.info("SolidityEditor::__init__ source_file_path=%s", source_file_path)

        self.source_file_path = source_file_path
        self.codes = None

    def load_code(self):
        with open(self.source_file_path, 'r') as f:
            self.codes = [format_line_for_load(index, line) for index, line in enumerate(f.readlines())]

            return self.codes

        return None

    def get_code_lines(self):
        if self.codes is not None:
            return [format_line_for_load(index, line) for index, line in enumerate(self.codes)]

        return self.load_code()

    def get_code(self):
        codes = self.get_code_lines()
        if codes is not None:
            return ''.join(codes)

        return None

    def get_code_at(self, index):
        codes = self.get_code_lines()
        if codes is not None and index < len(codes):
            return codes[index]

        return None

    def save_code(self):
        self.codes = [format_line_for_save(line) for line in self.codes]

        logger.info("SolidityEditor::save_code")

        with open(self.source_file_path, 'w') as f:
            f.write(''.join(self.codes))
            logger.info("SolidityEditor::saved %d lines to %s", len(self.codes), self.source_file_path)

            return True

        return False

    def add_codes(self, index, appending_codes):
        logger.info("SolidityEditor::add_codes index=%d new_codes=%d", index, len(appending_codes))

        current_codes = self.get_code_lines()

        new_codes = current_codes[:index] + appending_codes + current_codes[index:]

        self.codes = new_codes

        self.save_code()

        return self.codes

    def change_code(self, index, new_code):
        logger.info("SolidityEditor::replace_code index=%d, new_codes=%d", index, len(new_code))

        self.codes[index] = new_code

        self.save_code()

    def delete_codes(self, index):
        logger.info("SolidityEditor::delete_codes index=%d", index)

        current_codes = self.get_code_lines()
        current_codes.pop(index)
        self.codes = current_codes

        self.save_code()
