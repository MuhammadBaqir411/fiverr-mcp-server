import os

from fiverr_mcp_server.mcp_server import mcp
import fiverr_mcp_server.tools  # noqa: F401


def main():
    transport = os.getenv("TRANSPORT", "streamable-http")
    port = int(os.getenv("PORT", "8000"))

    mcp.run(
        transport=transport,
        host="0.0.0.0",
        port=port,
    )


if __name__ == "__main__":
    main()
