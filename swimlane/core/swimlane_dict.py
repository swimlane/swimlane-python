"""Helper class to make Python play nice with Swimlane."""

try:  # pragma: no cover
    from collections import OrderedDict
except ImportError:  # pragma: no cover
    from ordereddict import OrderedDict


class SwimlaneDict(OrderedDict):
    """A helper class that knows about JSON.NET $type values."""

    def __init__(self, d):
        """Init a SwimlaneDict with a dict.

        The dict is recursively converted to a series of OrderDicts with all
        "$type" keys bubbled to the top. This allows a SwimlaneDict to be
        serialized to JSON in a way that is compliant with JSON.NET.

        Args:
            d (dict): An unordered dict.

        Returns:
            A SwimlaneDict
        """
        self._ordered(d)
        super(SwimlaneDict, self).__init__(sorted(d.items()))

    def _ordered(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = OrderedDict(sorted(v.items()))
                self._ordered(d[k])
