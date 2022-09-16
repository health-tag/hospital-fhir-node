import re


def get_file_encoding(file_path):
    with open(file_path) as xml_file_for_encoding_check:
        first_line = xml_file_for_encoding_check.readline()
        encoding = re.search('encoding="(.*)"', first_line).group(1)
        if encoding == "windows-874":
            encoding = "cp874"
        return encoding
