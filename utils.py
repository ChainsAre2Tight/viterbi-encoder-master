def hamming_distance(string1: str, string2: str) -> int:
    assert len(string1) == len(string2)

    return sum([
        0 if string1[i] == string2[i] else 1 for i in range(len(string1))
    ])


class Pathfinder:

    @staticmethod
    def find_path_ending_in_vertex(
            vertex: str,
            paths: dict[tuple[str, str]: dict[str: int]]
    ) -> list[tuple[str, str]]:
        res = list()
        for edge in paths.keys():
            if edge[1] == vertex:
                res.append(edge)

        if len(res) == 0:
            raise KeyError(f'No paths end in ({vertex})')

        return res

    @staticmethod
    def find_path_beginning_in_vertex(
            vertex: str,
            paths: dict[tuple[str, str]: dict[str: int]]
    ) -> list[tuple[str, str]]:
        res = list()
        for edge in paths.keys():
            if edge[0] == vertex:
                res.append(edge)

        if len(res) == 0:
            raise KeyError(f'No paths begin in ({vertex})')

        return res
