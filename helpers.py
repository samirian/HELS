def read_configuration(filename: str):
	"""Reads a configutation file and returns the parameters as a dictionary.
	"""
	configuration = {}
	with open(filename) as configuration_file:
		for line in configuration_file.readlines():
			row = line.replace('\t', '').replace('\n', '').split('=', 1)

			if len(row) == 2:
				row[0] = remove_front_and_back_spaces(row[0])
				row[1] = remove_front_and_back_spaces(row[1])
				configuration[row[0]] = row[1]
	return configuration


def remove_front_and_back_spaces(value: str):
	clean_value = ''
	i = 0
	while i < len(value):
		letter = value[i]
		if letter != ' ':
			clean_value = value[i:len(value)]
			value = clean_value
			break
		i += 1
	i = len(value) - 1
	while i > -1:
		letter = value[i]
		if letter != ' ':
			clean_value = value[0:i + 1]
			break
		i -= 1
	return clean_value
