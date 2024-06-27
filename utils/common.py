
from django.db import models
from django.http import QueryDict
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import UploadedFile

from collections import defaultdict

"""
reusable functions
"""

def get_name_from_email(email):
    name, domain = email.split('@')
    return name.replace('.', ' ').strip().capitalize()


def get_file_size(request_file: UploadedFile, unit: str='MB'):
    """
    Get the file size from a file uploaded via request.FILES and convert it to KB or MB.

    """
    if unit not in ('KB', 'MB'):
        raise ValueError("Invalid unit. Please use 'KB' or 'MB'.")

    file_size_bytes = request_file.size

    if unit == 'MB':
        file_size = file_size_bytes / (1024 * 1024)  # 1 MB = 1024 KB
    else:
        file_size = file_size_bytes / 1024  # 1 KB = 1024 bytes

    return file_size


def generate_uniqueid(table: models.Model, field: str, length=12):

    unique_id = get_random_string(length=length)    

    while table.objects.filter(**{field: unique_id}).exists():
        unique_id = get_random_string(length=length)    

    return unique_id


def get_file_name(file_path: str):
    """
        given a string path returns the file name
    """

    name = file_path.split("/")

    return name[0].split(".")[0]


def form_parser(post_data: QueryDict):
    """
        Parses a form key into key value pair
        eg: 'work_experience[start_date]': [''], 'work_experience[end_date]': [''] ->
        {work_experience: [{start_date: "", end_date: ""}, {start_date: "", end_date:""}, ...]}

        key here is work_experience
    """
    nested_fields_data = defaultdict(list)

    for key, values in post_data.lists():
        
        if "[" in key:
            main_key, sub_key, *_ = key.split('[')
            sub_key = sub_key.rstrip("]") 
            # print("Keys: ", main_key, sub_key)
            if main_key not in nested_fields_data:
                nested_fields_data[main_key] = []   

            for idx, value in enumerate(values):
                # print("value: ", value, idx)

                if len(nested_fields_data[main_key]) <= idx:
                    nested_fields_data[main_key].append({sub_key: value})

                else:
                    nested_fields_data[main_key][idx].update({sub_key: value})  # Append the value with the original key

        else:
            nested_fields_data[key] = values


    return dict(nested_fields_data)


def extract_path(path: str):
    """
    Given path returns a proper path, e.g., /docs#heading1 -> docs/
    """

    path_parts = path.split("#", 1)
    path_parts = path_parts[0].split("?", 1)

    path_components = path_parts[0].split("/")
    path_components = [component for component in path_components if component]

    result_path = '/'.join(path_components)

    if path.endswith('/'):
        result_path = result_path[:-1]

    return result_path


def get_language_name(extension):
    language_mapping = {
        'py': 'python',
        'js': 'javascript',
        'ts': 'typescript',
        'html': 'html',
        'css': 'css',
        'java': 'java',
        'c++': 'cpp',
        'cs': 'csharp',
        'plain': 'plaintext',
        'rs': 'rust',
        'rb': 'ruby',
        'kt': 'kotlin',
        'sql': 'sql',
        'swift': 'swift',
        'sh': 'shell',
    }

    return language_mapping.get(extension.lower(), extension.lower())


def get_email_from_string(emails: str) -> list:
    """
        given comma separated emails returns list
    """

    return [x.strip() for x in emails.replace(' ', '').split(',') if x.strip() != '']
