import os

from fiverr_mcp_server.mcp_server import mcp
import fiverr_mcp_server.tools  # noqa: F401


def main():
    transport = os.getenv("TRANSPORT", "streamable-http")
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
