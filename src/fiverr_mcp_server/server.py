import os

from fiverr_mcp_server.mcp_server import mcp
import fiverr_mcp_server.tools  # noqa: F401 - registers tools


def main():
    mcp.run(transport=os.getenv("TRANSPORT", "stdio"))


if __name__ == "__main__":
    main()
