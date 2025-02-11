# see license/LICENSE.rst

try:
    from .version import __version__
except ImportError:
    __version__ = "unknown"


from hermes_core.util.config import load_config, print_config
from hermes_core.util.logger import _init_log

# Load user configuration
config = load_config()

log = _init_log(config=config)

# Then you can be explicit to control what ends up in the namespace,
__all__ = ["config", "print_config"]
