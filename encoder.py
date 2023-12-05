class RoadEndError(Exception):
    pass


class BinaryEncoder:
    _upper: list[int]
    _lower: list[int]
    _k: int

    def __init__(self, upper: str, lower: str):
        assert len(upper) == len(lower)
        self._upper = [i for i, val in enumerate(upper) if val == '1']
        self._lower = [i for i, val in enumerate(lower) if val == '1']
        self._k = len(upper)

    def encode(self, sequence: str) -> str:
        upper = 0
        for i in self._upper:
            upper = int(sequence[i]) ^ upper
        lower = 0
        for i in self._lower:
            lower = int(sequence[i]) ^ lower

        return f'{upper}{lower}'

    @property
    def k(self):
        return self._k


def hamming_distance(string1: str, string2: str) -> int:
    assert len(string1) == len(string2)

    return sum([
        0 if string1[i] == string2[i] else 1 for i in range(len(string1))
    ])


class Pathfinder:

    @staticmethod
    def find_path_ending_in_vertex(vertex: str, paths: dict) -> list[tuple[str, str]]:
        res = list()
        for edge in paths.keys():
            if edge[1] == vertex:
                res.append(edge)

        if len(res) == 0:
            raise KeyError(f'No paths end in ({vertex})')

        return res

    @staticmethod
    def find_path_beginning_in_vertex(vertex: str, paths: dict) -> list[tuple[str, str]]:
        res = list()
        for edge in paths.keys():
            if edge[0] == vertex:
                res.append(edge)

        if len(res) == 0:
            raise KeyError(f'No paths begin in ({vertex})')

        return res


class Grid:
    _paths: dict
    _encoder: BinaryEncoder

    def create_grid(self):
        for vertex_index in range(2 ** (self._encoder.k - 1)):
            vertex = str('{0:0' + str(self._encoder.k - 1) + 'b}').format(vertex_index)
            for addendum in 0, 1:
                exit_vertex = f'{addendum}{vertex}'[:-1]
                edge = (vertex, exit_vertex)
                encoded = self._encoder.encode(f'{addendum}{vertex}')
                dibit_format = '{0:02b}'
                distances = {
                    dibit_format.format(i): hamming_distance(dibit_format.format(i), encoded)
                    for i in range(4)
                }

                self._paths[edge] = distances

    def purge_grid(self):

        for exit_vertex_index in range(2 ** (self._encoder.k - 1)):
            exit_vertex = str('{0:0' + str(self._encoder.k - 1) + 'b}').format(exit_vertex_index)
            paths_to_thread = Pathfinder.find_path_ending_in_vertex(exit_vertex, self._paths)

            for i in range(4):
                dibit = '{0:02b}'.format(i)

                min_difference = min([
                    self._paths[path][dibit]
                    for path in paths_to_thread
                ])

                for path in paths_to_thread:
                    if self._paths[path][dibit] != min_difference:
                        self._paths[path].pop(dibit)

    def __init__(self, encoder: tuple[str, str] | BinaryEncoder):

        if isinstance(encoder, BinaryEncoder):
            self._encoder = encoder
        else:
            self._encoder = BinaryEncoder(*encoder)

        self._paths = dict()
        self.create_grid()
        self.purge_grid()

    @property
    def paths(self):
        return self._paths


class Encoder:
    _grid: Grid
    _binary_encoder: BinaryEncoder

    def __init__(self, encoder: tuple[str, str] | BinaryEncoder):
        if isinstance(encoder, BinaryEncoder):
            self._binary_encoder = encoder
        else:
            self._binary_encoder = BinaryEncoder(*encoder)

        self._grid = Grid(encoder=self._binary_encoder)

    @property
    def grid(self) -> Grid:
        return self._grid

    def encode(self, message: str) -> list[str]:
        assert set(message) == {'0', '1'}

        result = list()
        start_vertex = '0' * (self._binary_encoder.k - 1)
        vertex = start_vertex
        for bit in message:
            result.append(self._binary_encoder.encode(f'{bit}{vertex}'))
            print(vertex, f'{bit}{vertex}'[:-1], self._binary_encoder.encode(f'{bit}{vertex}'))
            vertex = f'{bit}{vertex}'[:-1]

        return result

    def decode(self, encoded_message: list[str], maximum_depth: int) -> str:

        def find_lowest_path_metric(
                depth: int,
                vertex: str,
                sequence: list[str],
                position: int,
                grid: Grid,
                metric: int
        ) -> int:
            if depth == 0 or position >= len(sequence) - 1:
                return metric
            try:
                dibit = sequence[position]
            except IndexError:
                print('lox', sequence, len(sequence), position)

            paths_to_tread = Pathfinder.find_path_beginning_in_vertex(vertex, grid.paths)

            min_metric = 99999
            flag = False
            for path in paths_to_tread:
                try:
                    flag = True
                    min_metric = min(min_metric, grid.paths[path][dibit])
                except KeyError:
                    continue
            if not flag:
                raise RoadEndError

            potential_paths = list()
            for path in paths_to_tread:
                try:
                    if grid.paths[path][dibit] == min_metric:
                        potential_paths.append(path)
                except KeyError:
                    continue

            assert len(potential_paths) > 0

            return min([
                find_lowest_path_metric(
                    depth=depth - 1,
                    vertex=path[1],
                    sequence=sequence,
                    position=position + 1,
                    grid=grid,
                    metric=metric + grid.paths[path][dibit]
                )
                for path in potential_paths
            ])

        def find_next_step(
                vertex: str,
                sequence: list[str],
                position: int,
                maximum_depth: int,
                grid: Grid
        ) -> str:
            paths_to_tread = Pathfinder.find_path_beginning_in_vertex(vertex=vertex, paths=grid.paths)
            min_metric = 99999
            result = None

            for path in paths_to_tread:
                try:
                    path_metric = find_lowest_path_metric(
                        depth=maximum_depth,
                        vertex=path[1],
                        sequence=sequence,
                        position=position + 1,
                        grid=grid,
                        metric=grid.paths[path][encoded_message[position]]
                    )
                except KeyError:
                    continue
                print('    ', path, path_metric)
                if path_metric < min_metric:
                    min_metric = path_metric
                    result = path[1]

            return result

        assert maximum_depth > 0
        result = ''
        vertex = '0' * (self._binary_encoder.k - 1)
        for position in range(len(encoded_message)):
            print(vertex, encoded_message[position])
            vertex = find_next_step(
                vertex=vertex,
                sequence=encoded_message,
                position=position,
                maximum_depth=maximum_depth,
                grid=self._grid,
            )
            result = result + vertex[0]

        return result


if __name__ == "__main__":
    encoder = Encoder(('1101', '1111'))
    print(*((key, value) for key, value in encoder.grid.paths.items()), sep='\n')
