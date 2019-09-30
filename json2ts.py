#!/usr/bin/env python
# copyright 2019 Nicolò Santamaria

import os
import sys
import json
import argparse


def write_ts_interface(name, content, outdir="./"):
	if outdir[-1] != "/":
		outdir += "/"

	iname = "I{}".format(name)
	filename = "{}{}.d.ts".format(outdir, iname)
	output = "export default interface {} {{\n".format(iname)

	for key in content.keys():

		if type(content[key]) is dict:
			iname_tmp = "I{}".format(key.title())
			output = "import {name} from './{name}';\n{out}\t{k}: {name};\n".format(name=iname_tmp, out=output, k=key)
			write_ts_interface(iname_tmp[1:], content[key], outdir)

		elif type(content[key]) is list:
			tmp = content[key]
			if len(tmp):
				if type(tmp[0]) is dict:
					iname_tmp = "I{}".format(key.title())
					output = "import {name} from './{name}';\n{out}\t{k}: {name}[];\n".format(name=iname_tmp, out=output, k=key)
					write_ts_interface(iname_tmp[1:], tmp[0], outdir)

				else:
					output += "\t{}: {}[];\n".format(key, str(content[key]))

		else:
			output += "\t{}: {};\n".format(key, content[key])

	output += "}\n"
	with open(filename, "w") as file:
		file.write(output)

	print(filename)


def parse_json_file(filepath, outdir="./"):
	filename = os.path.basename(filepath)
	tsname = filename

	if ".json" in filename:
		for s in ("DTO", "_", ".json"):
			tsname = tsname.replace(s, "");

		try:
			with open(filepath) as jfile:
				content = json.load(jfile)
				write_ts_interface(tsname, content, outdir)
		except Exception as e:
			print(filename, e)


def init_parser():
	parser = argparse.ArgumentParser(description="Convert json to typescript interface")
	parser.add_argument("inputFile", help="Path to the json files", nargs="*")
	parser.add_argument("-o", "--output", help="Output directory")

	return parser


def main():
	parser = init_parser()
	parser = parser.parse_args(sys.argv[1:])

	if parser.output and os.path.exists(parser.output):
		outdir = parser.output
	else:
		outdir = "./"

	for file in parser.inputFile:
		if os.path.exists(file):
			parse_json_file(file, outdir)


if __name__ == "__main__":
	main()
