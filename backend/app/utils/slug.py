import re
import uuid

def generate_slug(title: str, existing_slugs: list = None) -> str:
    """
    Generate a URL-friendly slug from a title.
    If the slug already exists, append a unique identifier.
    """
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower())
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # If no existing slugs provided, return the basic slug
    if not existing_slugs:
        return slug
    
    # If slug exists, append a unique identifier
    if slug in existing_slugs:
        unique_id = str(uuid.uuid4())[:8]
        return f"{slug}-{unique_id}"
    
    return slug 