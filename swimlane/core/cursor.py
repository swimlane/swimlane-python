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
    default_page_start = None
    default_page_end = None

    def __init__(self, limit=default_limit, page_size=default_page_size,
                 page_start=default_page_start, page_end=default_page_end):
        super(PaginatedCursor, self).__init__()

        self.__limit = limit
        self.page_size = page_size
        self.page_start = page_start
        self.page_end = page_end

        if self.__limit:
            self.page_size = min(self.page_size, self.__limit)

        if self.page_start and self.page_start <= 0:
            raise ValueError('page_start should be greater than 0')

        if self.page_end and self.page_end <= 0:
            raise ValueError('page_end should be greater than 0')

        if (self.page_start and self.page_end) and (self.page_start > self.page_end):
            raise ValueError('page_end cannot be less than page_start')

        if (self.page_start or self.page_end) and self.__limit != 0:
            raise ValueError(' page_start or page_end param is applicable only when limit is 0')

    def _evaluate(self):
        """Lazily retrieve and paginate report results and build Record instances from returned data"""
        if self._elements:
            for element in self._elements:
                yield element
        else:
            # Determine pagination range based on parameters
            if self.page_start and self.page_end:
                page_range = range(self.page_start-1, self.page_end)
            elif self.page_start:
                page_range = itertools.count(self.page_start-1)
            elif self.page_end:
                page_range = range(0, self.page_end)
            else:
                page_range = itertools.count()

            for page in page_range:
                raw_elements = self._retrieve_raw_elements(page)

                for raw_element in raw_elements:
                    element = self._parse_raw_element(raw_element)
                    self._elements.append(element)
                    yield element

                    if self.__limit and len(self._elements) >= self.__limit:
                        break

                # Break conditions for ending pagination
                if any([
                    len(raw_elements) < self.page_size,
                    self.__limit and len(self._elements) >= self.__limit,
                    self.page_size == 0
                ]):
                    break

    def _retrieve_raw_elements(self, page):
        """Send request and return response for single page of data"""
        raise NotImplementedError

    def _parse_raw_element(self, raw_element):
        """Hook to override parsing individual raw elements just before yielding"""
        return raw_element
