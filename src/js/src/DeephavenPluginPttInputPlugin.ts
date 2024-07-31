import { type WidgetPlugin, PluginType } from '@deephaven/plugin';
import { vsGraph } from '@deephaven/icons';
import { DeephavenPluginPttInputView } from './DeephavenPluginPttInputView';

// Register the plugin with Deephaven
export const DeephavenPluginPttInputPlugin: WidgetPlugin = {
  // The name of the plugin
  name: 'deephaven-plugin-ptt-input',
  // The type of plugin - this will generally be WIDGET_PLUGIN
  type: PluginType.WIDGET_PLUGIN,
  // The supported types for the plugin. This should match the value returned by `name`
  // in DeephavenPluginPttInputType in deephaven_plugin_ptt_input_type.py
  supportedTypes: 'DeephavenPluginPttInput',
  // The component to render for the plugin
  component: DeephavenPluginPttInputView,
  // The icon to display for the plugin
  icon: vsGraph,
};

export default DeephavenPluginPttInputPlugin;
