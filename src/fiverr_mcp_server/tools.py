import logging
from typing import Literal

from fiverr_mcp_server.mcp_server import mcp, scraper
from fiverr_mcp_server.models import (
    Category,
    Certification,
    GigDetails,
    GigSummary,
    Package,
    Review,
    ReviewsResult,
    SearchResult,
    SellerInfo,
    SellerProfile,
    Language,
    SellerGig,
)
from fiverr_mcp_server.utils.scraper import FIVERR_CATEGORIES

logger = logging.getLogger(__name__)

CategorySlug = Literal[
    "",
    "graphics-design",
    "programming-tech",
    "digital-marketing",
    "video-animation",
    "writing-translation",
    "music-audio",
    "business",
    "consulting",
    "ai-services",
    "personal-growth",
]


@mcp.tool()
def search_gigs(
    query: str,
    category: CategorySlug = "",
    min_price: int | None = None,
    max_price: int | None = None,
    seller_level: Literal["", "level_one_seller", "level_two_seller", "top_rated_seller"] = "",
    sort_by: Literal["relevance", "best_selling", "newest", "price_asc", "price_desc"] = "relevance",
    page: int = 1,
) -> SearchResult:
    """Search Fiverr gigs by keyword. Returns up to 48 gigs per page. All prices in USD.

    Use the gig URL from results with get_gig_details() for full pricing.
    Use the seller_name from results with get_seller_profile() for seller info.

    Args:
        query: Search query (e.g. "logo design", "python developer")
        category: Category slug to filter by (leave empty for all categories)
        min_price: Minimum price in USD
        max_price: Maximum price in USD
        seller_level: Filter by seller level
        sort_by: Sort order for results
        page: Page number (starts at 1)
    """
    try:
        data = scraper.search_gigs(
            query=query, category=category, min_price=min_price,
            max_price=max_price, seller_level=seller_level,
            sort_by=sort_by, page=page,
        )
        return SearchResult(
            gigs=[GigSummary(**g) for g in data.get("gigs", [])],
            query=data.get("query", query),
            page=data.get("page", page),
            total_results=data.get("total_results", 0),
            has_more=data.get("has_more", False),
            error=data.get("error"),
        )
    except Exception as e:
        logger.exception("search_gigs failed")
        return SearchResult(query=query, page=page, error=f"Search failed: {e}")


@mcp.tool()
def get_gig_details(url: str) -> GigDetails:
    """Get full details of a Fiverr gig including all pricing tiers (Basic/Standard/Premium).

    All prices in USD. Use the seller username from results with get_seller_profile() for more seller info.

    Args:
        url: Fiverr gig URL (e.g. "https://www.fiverr.com/username/gig-slug") or path ("username/gig-slug")
    """
    try:
        data = scraper.get_gig_details(url)
        if data.get("error"):
            return GigDetails(url=data.get("url", url), error=data["error"])

        seller_data = data.get("seller", {})
        packages_data = data.get("packages", [])

        return GigDetails(
            url=data.get("url", url),
            title=data.get("title", ""),
            description=data.get("description", ""),
            seller=SellerInfo(**seller_data) if seller_data else SellerInfo(),
            packages=[Package(**p) for p in packages_data],
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
            rating=data.get("rating", 0.0),
            reviews_count=data.get("reviews_count", 0),
            category=data.get("category", ""),
            sub_category=data.get("sub_category", ""),
            orders_in_queue=data.get("orders_in_queue", 0),
        )
    except Exception as e:
        logger.exception("get_gig_details failed")
        return GigDetails(url=url, error=f"Failed to fetch gig details: {e}")


@mcp.tool()
def get_seller_profile(username: str) -> SellerProfile:
    """Get a Fiverr seller's profile including bio, languages, certifications, and gig listings.

    Use the seller_name from search_gigs() results as the username here.

    Args:
        username: Seller's Fiverr username (e.g. "johndoe")
    """
    try:
        data = scraper.get_seller_profile(username)
        if data.get("error"):
            return SellerProfile(username=username, error=data["error"])

        languages = [
            Language(**lang) for lang in data.get("languages", [])
            if isinstance(lang, dict)
        ]
        gigs = [
            SellerGig(**g) for g in data.get("gigs", [])
            if isinstance(g, dict)
        ]
        certs = [
            Certification(**c) for c in data.get("certifications", [])
            if isinstance(c, dict)
        ]

        return SellerProfile(
            username=data.get("username", username),
            url=data.get("url", ""),
            display_name=data.get("display_name", ""),
            bio=data.get("bio", ""),
            location=data.get("location", ""),
            member_since=data.get("member_since", ""),
            response_time=data.get("response_time", ""),
            description=data.get("description", ""),
            languages=languages,
            gigs=gigs,
            certifications=certs,
            hourly_rate=data.get("hourly_rate", 0),
            approved_gigs_count=data.get("approved_gigs_count", 0),
            is_verified=data.get("is_verified", False),
        )
    except Exception as e:
        logger.exception("get_seller_profile failed")
        return SellerProfile(username=username, error=f"Failed to fetch profile: {e}")


@mcp.tool()
def get_gig_reviews(url: str) -> ReviewsResult:
    """Get reviews for a Fiverr gig. Returns the first page of reviews only (typically 5-10 reviews).

    Args:
        url: Fiverr gig URL (e.g. "https://www.fiverr.com/username/gig-slug") or path
    """
    try:
        data = scraper.get_gig_reviews(url)
        return ReviewsResult(
            reviews=[Review(**r) for r in data.get("reviews", [])],
            url=data.get("url", ""),
            error=data.get("error"),
        )
    except Exception as e:
        logger.exception("get_gig_reviews failed")
        return ReviewsResult(url=url, error=f"Failed to fetch reviews: {e}")


@mcp.tool()
def list_categories() -> list[Category]:
    """List all available Fiverr category slugs. Use these slugs with the category parameter in search_gigs()."""
    return [
        Category(slug=slug, name=name)
        for slug, name in FIVERR_CATEGORIES.items()
    ]
