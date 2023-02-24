def filter_schema_apis(endpoints):
    """
    Used to filter out certain API endpoints from the auto-generated docs / clients
    """
    return [e for e in endpoints if include_in_schema(e)]


def include_in_schema(endpoint):
    urL_path = endpoint[0]
    return not urL_path.startswith("/cms/")  # filter out wagtail URLs if present
