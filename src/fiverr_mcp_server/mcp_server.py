import os

from mcp.server.fastmcp import FastMCP

from fiverr_mcp_server.utils.scraper import FiverrScraper

mcp = FastMCP(
    "Fiverr",
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8000")),
)

scraper = FiverrScraper()
