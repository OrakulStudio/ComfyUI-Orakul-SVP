from .orakul_svp_node import OrakulSVPNode

NODE_CLASS_MAPPINGS = {
    "OrakulSVPNode": OrakulSVPNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OrakulSVPNode": "🎞️⚙️Orakul Motion Engine (SVP Flow)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']