from plugin_manager import PluginManager

manager = PluginManager()
manager.load_plugins()

for plugin in manager.get_plugins():
    print(plugin.get_name())
