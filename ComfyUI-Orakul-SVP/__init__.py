from .orakul_svp_node import OrakulSVPNode
from .orakul_injector import OrakulMetadataInjector

NODE_CLASS_MAPPINGS = {
    "OrakulSVPNode": OrakulSVPNode,
    "OrakulMetadataInjector": OrakulMetadataInjector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OrakulSVPNode": "🎞️⚙️Orakul SVP Engine",
    "OrakulMetadataInjector": "💉⚙️Orakul Metadata Injector"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']