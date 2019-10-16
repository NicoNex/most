#!/usr/bin/env python
# ATW: Automatic Test Writer
# copyright 2019 Nicolò Santamaria

import os
import re
import sys
from pathlib import Path

def find_substrings(string, subs):
    for s in subs:
        if s not in string:
            return False

    return True

def seek_props(path):
    # regex: export interface (.*) {\n(    (?:.+);)+\n}
    regex = r"export interface (.*) {\n(    (?:.+);)+\n}"
    regex2 = r"export interface (.*)Props {\n(    (?:.+);)+\n}"
    regex3 = r"export interface (.*)Props {\n(    (?:.+)?)+\n}"
    shit = "export interface"
    text = ""
    props = ""

    try:
        is_match = False

        with open("{}/index.tsx".format(path), "r") as file:
            # file_content = file.read()
            # # pattern = re.compile(regex)
            # matches = re.findall(regex3, file_content)
            # print(matches)
            line = file.readline()
            while line != "\0":
                if find_substrings(line, ("export", "interface", "Props", "{")):
                    is_match = True
                    break

                line = file.readline()

            if is_match:
                line = file.readline()
                while line not in ("}\n", "\0"):
                    text += line
                    line = file.readline()
    except Exception as e:
        print(e)

    print(text)

def write_test_file(path, props):
    component_name = str(path).split("\\")[-3]
    imp_text = "import {{ shallow }} from 'enzyme';\nimport React from 'react';\nimport {} from '..';\n\n".format(component_name)

    body = """describe('{comp}', () => {{
    it('Snapshot should be valid', () => {{
        const component = shallow(<{comp} {props} />);
        expect(component).toMatchSnapshot();
    }});
}});
""".format(comp=component_name, props=props)

    # print(imp_text + body)


def read_dir(dir):
    filename = "{}/__test__/index.test.tsx".format(dir)
    file_path = Path(filename)

    if not file_path.exists():
        print("Creating: {}".format(file_path))
        open(file_path, "a").close()

    props = seek_props(dir)
    # write_test_file(file_path, props)

def main():
    dirs = sys.argv[1:]

    for d in dirs:
        if os.path.isdir(d):
            read_dir(d)


if __name__ == "__main__":
    main()
