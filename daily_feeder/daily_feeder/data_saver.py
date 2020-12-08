

DATA_FILE = 'daily_feeder.properties'


def read():
    """Returns a dictionary of values stored in DATA_FILE

    ARGS: NONE
    RETURN: Dictionary of String: String values
    """

    properties = {}
    try:
        with open(DATA_FILE, 'r') as f:
            for line in f.readlines():
                values = line.split(':', maxsplit=1)
                if len(values) >= 2:
                    properties[values[0]] = values[1].strip()
    except FileNotFoundError:
        # Ignore
        pass

    return properties


def write(values, clean=False):
    """Writes the dictionary values to DATA_FILE. Normally this read
    existing values and then overwrite 'values' on top of that. It will
    then write the combined dictionary.

    ARGS:
        values: Dictionary to write.
        clean: Nuke old file

    Return: None
        """

    properties = {} if clean else read()
    properties.update(values)

    print("WRITING PROPERTIES", properties)
    with open(DATA_FILE, 'w') as f:
        for key, value in properties.items():
            f.write(f'{key}: {value}\n')
