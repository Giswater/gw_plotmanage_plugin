"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""
import configparser

from .. import global_vars
from ..settings import giswater_folder, tools_qgis, tools_log, tools_qt, tools_gw,tools_pgdao,tools_db


def get_config_parser(section: str, parameter: str, config_type, file_name, prefix=True, get_comment=False,
                      chk_user_params=True, get_none=False, force_reload=False) -> str:
    """ Load a simple parser value """

    if config_type not in ("user", "project"):
        tools_log.log_warning(f"get_config_parser: Reference config_type = '{config_type}' it is not managed")
        return None

    # Get configuration filepath and parser object
    path = global_vars.configs[file_name][0]
    parser = global_vars.configs[file_name][1]

    # Needed to avoid errors with giswater plugins
    if path is None:
        tools_log.log_warning(f"get_config_parser: Config file is not set")
        return None

    value = None
    raw_parameter = parameter
    if parser is None:
        tools_log.log_info(f"Creating parser for file: {path}")
        parser = configparser.ConfigParser(comment_prefixes=";", allow_no_value=True)
        parser.read(path)

    # If project has already been loaded and filename is 'init' or 'session', always read and parse file
    if force_reload or (global_vars.project_loaded and file_name in ('init', 'session')):
        parser = configparser.ConfigParser(comment_prefixes=";", allow_no_value=True)
        parser.read(path)

    if config_type == 'user' and prefix and global_vars.project_type is not None:
        parameter = f"{global_vars.project_type}_{parameter}"

    if not parser.has_section(section) or not parser.has_option(section, parameter):
        if chk_user_params and config_type in "user":
            value = _check_user_params(section, raw_parameter, file_name, prefix=prefix)
            set_config_parser(section, raw_parameter, value, config_type, file_name, prefix=prefix, chk_user_params=False)
    else:
        value = parser[section][parameter]

    # If there is a value and you don't want to get the comment, it only gets the value part
    if value is not None and not get_comment:
        value = value.split('#')[0].strip()

    if not get_none and str(value) in "None":
        value = None

    # Check if the parameter exists in the inventory, if not creates it
    if chk_user_params and config_type in "user":
        _check_user_params(section, raw_parameter, file_name, prefix)

    return value


def set_config_parser(section: str, parameter: str, value: str = None, config_type="user", file_name="session",
                      comment=None, prefix=True, chk_user_params=True):
    """ Save simple parser value """

    if config_type not in ("user", "project"):
        tools_log.log_warning(f"set_config_parser: Reference config_type = '{config_type}' it is not managed")
        return None

    # Get configuration filepath and parser object
    path = global_vars.configs[file_name][0]

    try:

        parser = configparser.ConfigParser(comment_prefixes=";", allow_no_value=True)
        parser.read(path)

        raw_parameter = parameter
        if config_type == 'user' and prefix and global_vars.project_type is not None:
            parameter = f"{global_vars.project_type}_{parameter}"

        # Check if section exists in file
        if section not in parser:
            parser.add_section(section)

        # Cast to str because parser only allow strings
        value = f"{value}"
        if value is not None:
            # Add the comment to the value if there is one
            if comment is not None:
                value += f" #{comment}"
            # If the previous value had an inline comment, don't remove it
            else:
                prev = get_config_parser(section, parameter, config_type, file_name, False, True, False)
                if prev is not None and "#" in prev:
                    value += f" #{prev.split('#')[1]}"
            parser.set(section, parameter, value)
            # Check if the parameter exists in the inventory, if not creates it
            if chk_user_params and config_type in "user":
                _check_user_params(section, raw_parameter, file_name, prefix)
        else:
            parser.set(section, parameter)  # This is just for writing comments

        with open(path, 'w') as configfile:
            parser.write(configfile)
            configfile.close()

    except Exception as e:
        tools_log.log_warning(f"set_config_parser exception [{type(e).__name__}]: {e}")
        return

def _check_user_params(section, parameter, file_name, prefix=False):
    """ Check if a parameter exists in the config/user_params.config
        If it doesn't exist, it creates it and assigns 'None' as a default value
    """

    if section == "i18n_generator" or parameter == "dev_commit":
        return

    # Check if the parameter needs the prefix or not
    if prefix and global_vars.project_type is not None:
        parameter = f"_{parameter}"

    # Get the value of the parameter (the one get_config_parser is looking for) in the inventory
    check_value = get_config_parser(f"{file_name}.{section}", parameter, "project", "user_params", False,
                                    get_comment=True, chk_user_params=False)
    # If it doesn't exist in the inventory, add it with "None" as value
    if check_value is None:
        set_config_parser(f"{file_name}.{section}", parameter, None, "project", "user_params", prefix=False,
                          chk_user_params=False)
    else:
        return check_value

