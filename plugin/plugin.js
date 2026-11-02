// Day Blocks: show the independent time-blocking view inside Super Productivity.
// Task and habit changes are made only through the documented PluginAPI.
(function () {
  'use strict';
  if (typeof PluginAPI === 'undefined') return;
  PluginAPI.registerMenuEntry({
    label: 'Day Blocks',
    icon: 'view_week',
    onClick: function () { PluginAPI.showIndexHtmlAsView(); }
  });
})();
