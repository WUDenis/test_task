from collections import namedtuple
from dataclasses import dataclass
from typing import Optional, Sequence, Tuple


Point = namedtuple("Point", ["x", "y"])


@dataclass
class WordSearch:
    words: Sequence[str]

    def __post_init__(self) -> None:
        self.forward_diagonals = ["" for _ in range(len(self.words[0]) + len(self.words) - 1)]
        self.backward_diagonals = ["" for _ in range(len(self.forward_diagonals))]
        self.forward_indices = [[] for _ in range(len(self.forward_diagonals))]  # type: ignore
        self.backward_indices = [[] for _ in range(len(self.forward_indices))]  # type: ignore

        for i in range(len(self.words[0])):
            for j in range(len(self.words)):
                forward_key = i + j
                self.forward_diagonals[forward_key] += self.words[j][i]
                self.forward_indices[forward_key].append((i, j))
                backward_key = i - j + len(self.words) - 1
                self.backward_diagonals[backward_key] += self.words[j][i]
                self.backward_indices[backward_key].append((i, j))

    def _search_rows(self, word: str) -> Optional[Tuple[Point, Point]]:
        for i, text in enumerate(self.words):
            if word in text:
                return Point(text.index(word), i), Point(text.index(word) + len(word) - 1, i)

            word_right = word[::-1]
            if word_right in text:
                return Point(len(word) - 1, i), Point(text.index(word_right), i)

        return None

    def _search_columns(self, word: str) -> Optional[Tuple[Point, Point]]:
        for i in range(len(self.words[0])):
            text = "".join([w[i] for w in self.words])
            if word in text:
                return Point(i, text.index(word)), Point(text.index(word) + len(word) - 1, i)

            text_rigth = text[::-1]
            if word in text_rigth:
                return Point(i, text_rigth.index(word) - 1), Point(i, text_rigth.index(word) - len(word))

        return None

    def _search_diagonals(self, word: str) -> Optional[Tuple[Point, Point]]:
        forward_diagonals = list(filter(lambda item: len(item) >= len(word), self.forward_diagonals))
        backward_diagonals = list(filter(lambda item: len(item) >= len(word), self.backward_diagonals))
        forward_indices = list(filter(lambda item: len(item) >= len(word), self.forward_indices))
        backward_indices = list(filter(lambda item: len(item) >= len(word), self.backward_indices))

        for text, indices in zip(forward_diagonals, forward_indices):
            if word in text:
                coordinates = indices[text.index(word) : text.index(word) + len(word)]
                return Point(*coordinates[0]), Point(*coordinates[-1])

            word_right = word[::-1]
            if word_right in text:
                coordinates = indices[text.index(word_right) : text.index(word_right) + len(word_right)]
                return Point(*coordinates[-1]), Point(*coordinates[0])

        for text, indices in zip(backward_diagonals, backward_indices):
            if word in text:
                coordinates = indices[text.index(word) : text.index(word) + len(word)]
                return Point(*coordinates[0]), Point(*coordinates[-1])

            word_right = word[::-1]
            if word_right in text:
                coordinates = indices[text.index(word_right) : text.index(word_right) + len(word_right)]
                return Point(*coordinates[-1]), Point(*coordinates[0])

        return None

    def search(self, word: str) -> Optional[Tuple[Point, Point]]:
        rows_result = self._search_rows(word)
        columns_result = self._search_columns(word)
        diagonals_result = self._search_diagonals(word)
        return rows_result or columns_result or diagonals_result
