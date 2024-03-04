import os


def test_empty():
    pass


def test_single_field():
    pass


def test_workers_json():
    directory_path = os.path.dirname(os.path.realpath(__file__))
    json_directory = os.path.join(directory_path, "json")
    json_files = os.listdir(json_directory)
    json_dict = {file_name.split(".")[0]: os.path.join(json_directory, file_name) for file_name in json_files}


def test_worker_addresses_json():
    pass
