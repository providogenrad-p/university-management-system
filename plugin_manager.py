"""Plug-in Manager: discovers, loads and validates report plug-ins.

The core never imports an individual plug-in. It only knows the contract:
    get_name() -> str
    generate(data) -> str   (path of the generated report)
"""

import importlib
import os

PLUGINS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")
PLUGINS_PACKAGE = "plugins"
REQUIRED_FUNCTIONS = ("get_name", "generate")


def discover_plugins():
    """Return the sorted list of plug-in file names (e.g. 'txt_report.py')."""
    if not os.path.isdir(PLUGINS_DIR):
        return []

    plugin_files = []
    for filename in os.listdir(PLUGINS_DIR):
        if not filename.endswith(".py"):
            continue
        if filename == "__init__.py":
            continue
        plugin_files.append(filename)
    return sorted(plugin_files)


def is_valid_plugin(module):
    """A plug-in is valid if it has callable get_name and generate."""
    return all(callable(getattr(module, name, None)) for name in REQUIRED_FUNCTIONS)


class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self):
        self.plugins = []

        for filename in discover_plugins():
            # txt_report.py -> plugins.txt_report
            module_name = f"{PLUGINS_PACKAGE}.{filename[:-3]}"

            try:
                module = importlib.import_module(module_name)
            except Exception as error:
                print(f"Could not load {module_name}: {error}")
                continue

            if not is_valid_plugin(module):
                missing = [n for n in REQUIRED_FUNCTIONS
                           if not callable(getattr(module, n, None))]
                print(f"Skipping {module_name}: not a valid plug-in "
                      f"(missing {', '.join(missing)})")
                continue

            self.plugins.append(module)

        return self.plugins

    def get_plugins(self):
        return self.plugins
