"""better_partial.py: contains BetterPartial class"""

from copy import copy

class BetterPartial:
    """
    BetterPartial -- rai.Partial with optionmap

    This is an improved version of the standard rai.Partial
    that also allows renaming options.
    So if the caller passes an option called `l`,
    but the compo expects it to be called `length`,
    you can use BetterPartial to resolve that.
    """

    compo_cls: 'rai.typing.CompoType'

    class Mapped(str):
        pass

    def __init__(
            self,
            compo_cls: 'rai.typing.CompoType',
            **kwargs
            ) -> None:

        self.compo_cls = compo_cls
        self.optmap = {}  # caller name -> callee name
        self.kwargs = {}

        for key, val in kwargs.items():
            if isinstance(val, self.Mapped):
                self.optmap[str(val)] = key
            else:
                self.kwargs[key] = val

    def __call__(self, **kwargs) -> 'rai.typing.Compo':
        """Finish creating the partially created Compo."""

        mapped_kwargs = {
            self.optmap.get(key, key) : val
            for key, val in kwargs.items()
            }
        kwargs2 = copy(self.kwargs)
        kwargs2.update(mapped_kwargs)
        return self.compo_cls(**kwargs2)

