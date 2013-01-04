__all__ = ['ImportLoader']

from glob import glob
import imp
import os
import sys

import logging
logger = logging.getLogger(__name__)

class ImportLoader:
    def load(self, search_path, extension='py'):
        if not isinstance(search_path, list):
            search_path = [search_path]
        logger.debug('Loading plugins with ImportLoader')
        for path in search_path:
            logger.debug("Searching for plugins in '%s'" % path)
            plugin_files = glob(os.path.join(path, '*.%s'%extension))

            # Note: for reproducibility, this fixes the order that
            # files are loaded
            for plugin_file in sorted(plugin_files):
                module=None
                plugin_name = os.path.basename(plugin_file)
                plugin_name,_ = os.path.splitext(plugin_name)
                if plugin_name not in sys.modules:
                    try:
                        logger.debug('Loading plugins from %s' % plugin_file)
                        module = imp.load_source(plugin_name, plugin_file)
                    except Exception:
                        e = sys.exc_info()[1]
                        logger.error('Failed to load plugin from %s', plugin_file, exc_info=True)
                        logger.error('Load error: %r' % str(e))

