from django.utils.text import slugify


def get_next_unique_slug(model_class, display_name, slug_field_name):
    """
    Gets the next unique slug based on the name. Appends -1, -2, etc. until it finds
    a unique value.
    """
    base_value = slugify(display_name)
    if model_class.objects.filter(slug=base_value).exists():
        # todo make this do fewer queries
        suffix = 2
        while True:
            next_slug = get_next_slug(base_value, suffix)
            if not model_class.objects.filter(**{slug_field_name: next_slug}).exists():
                return next_slug
            else:
                suffix += 1
    else:
        return base_value


def get_next_slug(base_value, suffix, max_length=100):
    """
    Gets the next slug from base_value such that "base_value-suffix" will not exceed max_length characters.
    """
    suffix_length = len(str(suffix)) + 1  # + 1 for the "-" character
    if suffix_length >= max_length:
        raise ValueError("Suffix {} is too long to create a unique slug! ".format(suffix))

    return "{}-{}".format(base_value[: max_length - suffix_length], suffix)
