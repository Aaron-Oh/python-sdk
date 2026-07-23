"""Resources primitive: a static URI, an RFC-6570 template, and a binary blob via @mcp.resource()."""

import base64

from mcp.server.mcpserver import MCPServer
from stories._hosting import run_server_from_args

# A 1x1 transparent GIF. Kept as bytes so the resource returns binary, not text.
TINY_GIF = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")


def build_server() -> MCPServer:
    mcp = MCPServer("resources-example")

    @mcp.resource("config://app", mime_type="application/json")
    def app_config() -> str:
        """Static application config."""
        return '{"feature": true}'

    @mcp.resource("greeting://{name}")
    def greeting(name: str) -> str:
        """A greeting for the named subject."""
        return f"Hello, {name}!"

    @mcp.resource("cover://placeholder", mime_type="image/gif")
    def placeholder_cover() -> bytes:
        """Return bytes, so the SDK sends BlobResourceContents (base64), not text."""
        return TINY_GIF

    return mcp


if __name__ == "__main__":
    run_server_from_args(build_server)
