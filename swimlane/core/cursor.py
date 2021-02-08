import itertools


class Cursor(object):

    def __init__(self):
        self._elements = []

    def __len__(self):
        return len(list(self._evaluate()))

    def __iter__(self):
        for element in self._evaluate():
            yield element

    def __getitem__(self, item):
        return self._evaluate()[item]

    def _evaluate(self):
        """Hook to allow lazy evaluation or retrieval of cursor's elements

        Defaults to simply returning list of self._elements
        """
        return self._elements


class PaginatedCursor(Cursor):
    """Handle paginated lists, exposes hooks to simplify retrieval and parsing of paginated data"""

    default_limit = 0
    default_page_size = 10

    def __init__(self, limit=default_limit, page_size=default_page_size):
        super(PaginatedCursor, self).__init__()

        self.__limit = limit
        self.page_size = page_size

        if self.__limit:
            self.page_size = min(self.page_size, self.__limit)

    def _evaluate(self):
        """Lazily retrieve and paginate report results and build Record instances from returned data"""
        if self._elements:
            for element in self._elements:
                yield element
        else:
            for page in itertools.count():
                raw_elements = self._retrieve_raw_elements(page)

                for raw_element in raw_elements:
                    element = self._parse_raw_element(raw_element)
                    self._elements.append(element)
                    yield element
                    if self.__limit and len(self._elements) >= self.__limit:
                        break

                if any([
                    (len(raw_elements) < self.page_size),
                    (self.__limit and len(self._elements) >= self.__limit),
                    (self.page_size == 0)
                ]):
                    break

    def _retrieve_raw_elements(self, page):
        """Send request and return response for single page of data"""
        raise NotImplementedError

    def _parse_raw_element(self, raw_element):
        """Hook to override parsing individual raw elements just before yielding"""
        return raw_element
