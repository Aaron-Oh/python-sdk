"""Resources primitive (lowlevel API): hand-built list/templates/read handlers."""

from typing import Any

import mcp_types as types
from mcp_types.jsonrpc import INVALID_PARAMS

from mcp.server.context import ServerRequestContext
from mcp.server.lowlevel import Server
from mcp.shared.exceptions import MCPError
from stories._hosting import run_server_from_args

# A 1x1 transparent GIF, already base64-encoded — BlobResourceContents.blob is a
# base64 string, so at this tier you supply it directly (no bytes round-trip).
TINY_GIF_B64 = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"


def build_server() -> Server[Any]:
    async def list_resources(
        ctx: ServerRequestContext[Any], params: types.PaginatedRequestParams | None
    ) -> types.ListResourcesResult:
        return types.ListResourcesResult(
            resources=[
                types.Resource(
                    uri="config://app",
                    name="app_config",
                    description="Static application config.",
                    mime_type="application/json",
                ),
                types.Resource(
                    uri="cover://placeholder",
                    name="placeholder_cover",
                    description="A 1x1 transparent GIF, returned as binary.",
                    mime_type="image/gif",
                ),
            ]
        )

    async def list_resource_templates(
        ctx: ServerRequestContext[Any], params: types.PaginatedRequestParams | None
    ) -> types.ListResourceTemplatesResult:
        return types.ListResourceTemplatesResult(
            resource_templates=[
                types.ResourceTemplate(
                    uri_template="greeting://{name}",
                    name="greeting",
                    description="A greeting for the named subject.",
                    mime_type="text/plain",
                )
            ]
        )

    async def read_resource(
        ctx: ServerRequestContext[Any], params: types.ReadResourceRequestParams
    ) -> types.ReadResourceResult:
        if params.uri == "config://app":
            text, mime = '{"feature": true}', "application/json"
        elif params.uri.startswith("greeting://"):
            text, mime = f"Hello, {params.uri.removeprefix('greeting://')}!", "text/plain"
        elif params.uri == "cover://placeholder":
            # Binary payload: a BlobResourceContents carrying the base64 string,
            # not a TextResourceContents. The client must narrow on the type.
            return types.ReadResourceResult(
                contents=[types.BlobResourceContents(uri=params.uri, mime_type="image/gif", blob=TINY_GIF_B64)]
            )
        else:
            raise MCPError(code=INVALID_PARAMS, message=f"Resource not found: {params.uri}")
        return types.ReadResourceResult(
            contents=[types.TextResourceContents(uri=params.uri, mime_type=mime, text=text)]
        )

    return Server(
        "resources-example",
        on_list_resources=list_resources,
        on_list_resource_templates=list_resource_templates,
        on_read_resource=read_resource,
    )


if __name__ == "__main__":
    run_server_from_args(build_server)
