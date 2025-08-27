def categorize(platform: str, payload: dict) -> str:
    if platform == "whatsapp": return "dm"
    if platform == "instagram":
        if "comment" in str(payload).lower(): return "comments"
        if "mention" in str(payload).lower(): return "mentions"
        return "activity"
    if platform in ("twitter","x"):
        return "mentions"
    return "general"
