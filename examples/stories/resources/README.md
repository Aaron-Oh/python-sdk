# resources

Expose data by URI: a static resource (`config://app`), an RFC-6570 template
(`greeting://{name}`), and a binary resource (`cover://placeholder`). One
`@mcp.resource()` decorator handles all three — the SDK infers
static-vs-template from whether the URI contains `{...}`, and text-vs-binary
from whether the function returns `str` or `bytes`. The client lists resources,
lists templates, then reads each.

## Run it

```bash
# stdio (default — the client spawns the server as a subprocess)
uv run python -m stories.resources.client

# HTTP — the client self-hosts the server on a free port, runs, then tears it down
uv run python -m stories.resources.client --http
# same, against the lowlevel-API server variant
uv run python -m stories.resources.client --http --server server_lowlevel
```

## What to look at

- `client.py` `async with Client(target, mode=mode) as client:` — the one line
  every client example exists to teach. `target` is anything `Client()`
  accepts (an in-process server, a transport, or an HTTP URL) and `mode=` is
  always explicit; the rest of the story is the body of that `async with`.
- `server.py` `app_config` vs `greeting` — a URI with no `{}` registers a
  static resource (appears in `resources/list`); a URI with `{name}` registers
  a template (appears only in `resources/templates/list`) and the placeholder
  must match the function parameter name.
- `server.py` `placeholder_cover` — returning `bytes` (not `str`) makes
  `MCPServer` emit a `BlobResourceContents` whose `.blob` is the base64 of those
  bytes; `mime_type=` labels the payload. The lowlevel server supplies the same
  base64 string by hand.
- `server_lowlevel.py` `read_resource` — without `MCPServer` you own the URI
  dispatch yourself, including raising `MCPError(code=INVALID_PARAMS, ...)` for
  unknown URIs (matches what `MCPServer` sends).
- `client.py` `isinstance(entry, TextResourceContents)` vs
  `BlobResourceContents` — `contents` is a list of
  `TextResourceContents | BlobResourceContents`; the text URIs yield the former
  (read `.text`), `cover://placeholder` yields the latter (base64-decode
  `.blob`). Narrow on the type before touching either field.

## Not shown here

Subscriptions. Per-URI `resources/subscribe` is a 2025-era RPC being replaced
by `subscriptions/listen` in 2026-07-28; neither is shown in this story. See
`stickynotes/` for `list_changed` notifications.

## Spec

[Resources — server features](https://modelcontextprotocol.io/specification/2025-11-25/server/resources)

## See also

`stickynotes/` (list-changed notifications), `pagination/` (cursor over a long
resource list).
