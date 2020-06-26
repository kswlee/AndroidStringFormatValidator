import os
from androidString import *
import json

check_result = {
	'is_error': False,
	'is_warning': False,
	'error': [],
	'warning': []
}


def list_strings():
	langs = ["es", "zh-rTW"]

	base_res_path = os.path.abspath(os.path.abspath(os.getcwd()) + "/../app/src/main/res/")
	strings_path = '{}'.format(base_res_path)

	i18n_base = Androidi18nStrings('{}/values/strings.xml'.format(strings_path), error_handler)

	for lang in langs:
		lang_str_path = '{}/values-{}/strings.xml'.format(strings_path, lang)
		i18n = Androidi18nStrings(lang_str_path, error_handler)
		i18n.match_ctrl_codes(i18n_base)

	print(json.dumps(check_result).decode('utf-8'))


def error_handler(error, warning):
	if error:
		check_result['is_error'] = True
		check_result['error'].append(error.decode('utf-8'))

	if warning:
		check_result['is_warning'] = True
		check_result['warning'].append(warning.decode('utf-8'))


def main():
	list_strings()


main()
