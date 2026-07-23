"""List resources and templates, then read the static, templated, and binary URIs."""

import base64

from mcp_types import BlobResourceContents, TextResourceContents

from mcp.client import Client
from stories._harness import Target, run_client


async def main(target: Target, *, mode: str = "auto") -> None:
    async with Client(target, mode=mode) as client:
        listed = await client.list_resources()
        assert [r.uri for r in listed.resources] == ["config://app", "cover://placeholder"]

        templates = await client.list_resource_templates()
        assert [t.uri_template for t in templates.resource_templates] == ["greeting://{name}"]

        config = await client.read_resource("config://app")
        entry = config.contents[0]
        assert isinstance(entry, TextResourceContents)
        assert entry.text == '{"feature": true}'
        assert entry.mime_type == "application/json"

        hello = await client.read_resource("greeting://world")
        entry = hello.contents[0]
        assert isinstance(entry, TextResourceContents)
        assert entry.text == "Hello, world!"

        # Binary resource: `contents` is TextResourceContents | BlobResourceContents,
        # so narrow on the type before touching `.blob` — reading `.text` here would fail.
        cover = await client.read_resource("cover://placeholder")
        entry = cover.contents[0]
        assert isinstance(entry, BlobResourceContents)
        assert entry.mime_type == "image/gif"
        assert base64.b64decode(entry.blob).startswith(b"GIF89a")


if __name__ == "__main__":
    run_client(main)
