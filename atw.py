#!/usr/bin/env python
# ATW: Automatic Test Writer
# copyright 2019 Nicolò Santamaria

import os
import re
import sys
# import argparse
from pathlib import Path
from colorama import Fore, Style

def print_err(e):
    print(Fore.RED + str(e) + Style.RESET_ALL)

def seek_props(path):
    regex = r"export interface [a-zA-Z]+Props {\n?([^}]+)\n?}"

    try:
        with open("{}/index.tsx".format(path), "r") as file:
            file_content = file.read()
            matches = re.findall(regex, file_content)
    except Exception as e:
        print_err(e)
        return None

    if len(matches) > 0:
        return matches[0].split("\n")

    return None

def write_test_file(path, props_txt):
    component_name = str(path).split("\\")[-3]
    text = """import {{ shallow }} from 'enzyme';
import React from 'react';
import {comp} from '..';

describe('{comp}', () => {{
    it('Snapshot should be valid', () => {{
        const component = shallow(<{comp} {props} />);
        expect(component).toMatchSnapshot();
    }});
}});
""".format(comp=component_name, props=props_txt)

    print(Fore.YELLOW + component_name)
    with open(path, "w") as file:
        file.write(text)
    # print(text)

def format_props(props, optional=False):
    assert type(props) is dict
    text = ""

    for k in props.keys():
        if "//" in k:
            continue

        if optional:
            text += "{}={} ".format(k.replace("?", ""), props[k])
        else:
            if "?" not in k:
                text += "{}={} ".format(k, props[k])

    return text


def read_dir(dir):
    filename = "{}/__test__/index.test.tsx".format(dir)
    file_path = Path(filename)
    props_dict = {}
    props_text = ""

    if not file_path.exists():
        print(Fore.YELLOW + "Creating: {}".format(file_path))
        open(file_path, "a").close()

    props = seek_props(dir)
    if props is None or props == []:
        props = ()
    else:
        props = props[:-1]

    for p in props:
        for s in (" ", ";"):
            p = p.replace(s, "")

        try:
            key, value = p.split(":")
        except Exception as e:
            print_err(e)
            print(p, dir)

        props_dict[key] = value

    props_text = format_props(props_dict, True)
    write_test_file(file_path, props_text)

# def init_parser():
# 	parser = argparse.ArgumentParser(description="Writes unit tests for you")
# 	parser.add_argument("inputDir", help="Path to the directories", nargs="*")
# 	parser.add_argument("-o", "--output", help="Output directory")
#
# 	return parser


def main():
    # parser = init_parser()
    dirs = sys.argv[1:]

    # if parser.output and os.path.exists(parser.output):
	# 	outdir = parser.output
	# else:
	# 	outdir = "./"

    for d in dirs:
        if os.path.isdir(d):
            read_dir(d)


if __name__ == "__main__":
    main()
