# deephaven_plugin_ptt_input

This is a Python plugin for Deephaven generated from a [deephaven-plugin](https://github.com/deephaven/deephaven-plugins) template.

Specifically, this plugin is a bidirectional widget plugin, which can send and receive messages on both the client and server.
The plugin works out of the box, demonstrates basic plugin structure, and can be used as a starting point for building more complex plugins.

## Plugin Structure

The `src` directory contains the Python and JavaScript code for the plugin.
Within the `src` directory, the deephaven_plugin_ptt_input directory contains the Python code, and the `js` directory contains the JavaScript code.

The Python files have the following structure:
`deephaven_plugin_ptt_input_object.py` defines a simple Python class that can send messages to the client.
`deephaven_plugin_ptt_input_type.py` defines the Python type for the plugin (which is used for registration) and a simple message stream.
`js_plugin.py` defines the Python class that will be used to setup the JavaScript side of the plugin.
`register.py` registers the plugin with Deephaven.

The JavaScript files have the following structure:
`DeephavenPluginPttInputPlugin.ts` registers the plugin with Deephaven.
`DeephavenPluginPttInputView.tsx` defines the plugin panel and message handling.

Additionally, the `test` directory contains Python tests for the plugin. This demonstrates how the embedded Deephaven server can be used in tests.
It's recommended to use `tox` to run the tests, and the `tox.ini` file is included in the project.

## Building the Plugin

To build the plugin, you will need `npm` and `python` installed, as well as the `build` package for Python.
`nvm` is also strongly recommended, and an `.nvmrc` file is included in the project.
The python venv can be created and the recommended packages installed with the following commands:
```sh
cd deephaven_plugin_ptt_input
python -m venv .venv
source .venv/bin/activate
pip install --upgrade -r requirements.txt
```

Build the JavaScript plugin from the `src/js` directory:

```sh
cd src/js
nvm install
npm install
npm run build
```

Then, build the Python plugin from the top-level directory:

```sh
cd ../..
python -m build --wheel
```

The built wheel file will be located in the `dist` directory.

If you modify the JavaScript code, remove the `build` and `dist` directories before rebuilding the wheel:
```sh
rm -rf build dist
```

## Installing the Plugin

The plugin can be installed into a Deephaven instance with `pip install <wheel file>`.
The wheel file is stored in the `dist` directory after building the plugin.
Exactly how this is done will depend on how you are running Deephaven.
If using the venv created above, the plugin and server can be created with the following commands:
```sh
pip install deephaven-server
pip install dist/deephaven_plugin_ptt_input-0.0.1.dev0-py3-none-any.whl
deephaven server
```
See the [plug-in documentation](https://deephaven.io/core/docs/how-to-guides/use-plugins/) for more information.

## Using the Plugin

Once the Deephaven server is running, the plugin should be available to use.

```python
from deephaven_plugin_ptt_input import DeephavenPluginPttInputObject

obj = DeephavenPluginPttInputObject()
```

A panel should appear. You can now use the object to send messages to the client.

```python
obj.send_message("Hello, world!")
```

The panel can also send messages back to the Python client by using the input field.

## Distributing the Plugin
To distribute the plugin, you can upload the wheel file to a package repository, such as [PyPI](https://pypi.org/).
The version of the plugin can be updated in the `setup.cfg` file.

There is a separate instance of PyPI for testing purposes.
Start by creating an account at [TestPyPI](https://test.pypi.org/account/register/).
Then, get an API token from [account management](https://test.pypi.org/manage/account/#api-tokens), setting the “Scope” to “Entire account”.

To upload to the test instance, use the following commands:
```sh
python -m pip install --upgrade twine
python -m twine upload --repository testpypi dist/*
```

Now, you can install the plugin from the test instance. The extra index is needed to find dependencies:
```sh
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ deephaven_plugin_ptt_input
```

For a production release, create an account at [PyPI](https://pypi.org/account/register/).
Then, get an API token from [account management](https://pypi.org/manage/account/#api-tokens), setting the “Scope” to “Entire account”.

To upload to the production instance, use the following commands. 
Note that `--repository` is the production instance by default, so it can be omitted:
```sh
python -m pip install --upgrade twine
python -m twine upload dist/*
```

Now, you can install the plugin from the production instance:
```sh
pip install deephaven_plugin_ptt_input
```

See the [Python packaging documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives) for more information.
