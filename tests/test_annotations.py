"""Annotation tests: every tool declares all four MCP behaviour hints
as explicit booleans matching the handler's real semantics (some
directories, e.g. OpenAI's, reject tools missing any of the four)."""

from __future__ import annotations

import asyncio

from token_verdict_mcp.server import mcp

EXPECTED = {
    # Pure read of live market data; nothing written server-side.
    "token_verdict": {
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
}


def test_all_tools_declare_all_four_hints():
    tools = asyncio.run(mcp.list_tools())
    assert {t.name for t in tools} == set(EXPECTED)
    for tool in tools:
        ann = tool.annotations
        assert ann is not None, tool.name
        got = {
            "readOnlyHint": ann.readOnlyHint,
            "destructiveHint": ann.destructiveHint,
            "idempotentHint": ann.idempotentHint,
            "openWorldHint": ann.openWorldHint,
        }
        assert all(isinstance(v, bool) for v in got.values()), (tool.name, got)
        assert got == EXPECTED[tool.name]
