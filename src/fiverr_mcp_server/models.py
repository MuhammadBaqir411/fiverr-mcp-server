from pydantic import BaseModel, Field


class GigSummary(BaseModel):
    title: str = ""
    seller_name: str = ""
    seller_level: str = Field("", description="e.g. level_one_seller, level_two_seller, top_rated_seller")
    price: float = Field(0, description="Starting price in USD")
    rating: float = 0.0
    reviews_count: int = 0
    url: str = ""


class Package(BaseModel):
    name: str = Field("", description="Tier name (e.g. Basic, Standard, Premium)")
    price: float = Field(0, description="Price in USD")
    description: str = ""
    delivery_days: int = 0
    revisions: int = Field(0, description="Number of revisions included (-1 means unlimited)")
    features: list[str] = Field(default_factory=list)


class SellerInfo(BaseModel):
    username: str = ""
    display_name: str = ""
    level: str = Field("", description="e.g. level_one_seller, level_two_seller, top_rated_seller")
    country: str = Field("", description="Two-letter country code")


class GigDetails(BaseModel):
    url: str = ""
    title: str = ""
    description: str = ""
    seller: SellerInfo = Field(default_factory=SellerInfo)
    packages: list[Package] = Field(default_factory=list, description="Pricing tiers (Basic/Standard/Premium)")
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, list[str]] = Field(default_factory=dict, description="Gig attributes like programming language, tools used")
    rating: float = 0.0
    reviews_count: int = 0
    category: str = ""
    sub_category: str = ""
    orders_in_queue: int = 0
    error: str | None = None


class Language(BaseModel):
    language: str = Field("", description="Language code (e.g. EN, ES, FR)")
    level: str = Field("", description="e.g. NATIVE_OR_BILINGUAL, FLUENT, CONVERSATIONAL, BASIC")


class Certification(BaseModel):
    name: str = ""
    received_from: str = Field("", alias="from")
    year: int = 0

    model_config = {"populate_by_name": True}


class SellerGig(BaseModel):
    title: str = ""
    url: str = ""
    rating: float = 0.0


class SellerProfile(BaseModel):
    username: str = ""
    url: str = ""
    display_name: str = ""
    bio: str = Field("", description="Short one-liner tagline")
    location: str = ""
    member_since: str = Field("", description="e.g. Jan 2023")
    response_time: str = ""
    description: str = Field("", description="Full profile description/about text")
    languages: list[Language] = Field(default_factory=list)
    gigs: list[SellerGig] = Field(default_factory=list)
    certifications: list[Certification] = Field(default_factory=list)
    hourly_rate: float = Field(0, description="Hourly rate in USD")
    approved_gigs_count: int = 0
    is_verified: bool = False
    error: str | None = None


class Review(BaseModel):
    buyer_name: str = ""
    country: str = ""
    rating: float = 0
    date: str = ""
    text: str = ""


class SearchResult(BaseModel):
    gigs: list[GigSummary] = Field(default_factory=list)
    query: str = ""
    page: int = 1
    total_results: int = 0
    has_more: bool = False
    error: str | None = None


class ReviewsResult(BaseModel):
    reviews: list[Review] = Field(default_factory=list)
    url: str = ""
    note: str = Field(
        "Only the first page of reviews is available (loaded from the gig page SSR data)",
        description="Limitation notice",
    )
    error: str | None = None


class Category(BaseModel):
    slug: str = ""
    name: str = ""
