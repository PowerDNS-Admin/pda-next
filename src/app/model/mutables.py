
class Mutable:
    """ Mutable objects are objects that can be modified after creation. """

    def __init__(self, *args, **kwargs):
        """ Initialize a mutable object. """
        super().__init__()
        for attr_name, attr_value in kwargs.items():
            if hasattr(self, attr_name):
                setattr(self, attr_name, attr_value)
            elif hasattr(self, f'_{attr_name}'):
                setattr(self, f'_{attr_name}', attr_value)

    def __getattr__(self, item: str):
        """ Return the value of an attribute. """
        if item.startswith('__') and item.endswith('__'):
            return getattr(super(), item)

        if item.startswith('_'):
            item = item[1:]
        if not hasattr(self, f'_{item}'):
            raise AttributeError(f'{self.__class__.__name__} has no attribute {item}')
        return getattr(self, f'_{item}')

    def __repr__(self):
        """ Return a string representation of the object. """
        props: list = [k for k in dir(self)
                       if not (k.startswith('__') and k.endswith('__')) and not callable(getattr(self, k))]
        return f'{self.__class__.__name__}({", ".join([f"{k}={getattr(self, k)}" for k in props])})'

    @classmethod
    def factory(cls, **kwargs):
        """ Create a new instance of the class. """
        return cls(**kwargs)
