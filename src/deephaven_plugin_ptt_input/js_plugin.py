import pathlib

from deephaven.plugin.js import JsPlugin

# This plugin allows the Python plugin to register a JavaScript plugin.
# The properties will be filled in during the registration process.
class DeephavenPluginPttInputJsPlugin(JsPlugin):
    def __init__(
        self,
        name: str,
        version: str,
        main: str,
        path: pathlib.Path,
    ) -> None:
        self._name = name
        self._version = version
        self._main = main
        self._path = path

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def main(self) -> str:
        return self._main

    def path(self) -> pathlib.Path:
        return self._path
