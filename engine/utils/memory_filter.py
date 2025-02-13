def filter_memories_by_score(memories: dict, threshold: float = 0) -> list:
    """Filter and sort memories by score"""
    if not memories or "matches" not in memories:
        return []

    high_score_matches = [
        match for match in memories["matches"] if match.get("score", 0) >= threshold
    ]

    return sorted(high_score_matches, key=lambda x: x.get("score", 0), reverse=True)
