def get_raw_data(file_path: str) -> str:
    """Returns the raw data from a path

    :param file_path: filepath for data
    :type file_path: str

    :return: Raw text input for example
    :rtype: str
    """

    with open(file_path, "r") as file:
        data = file.read()
    return data
