from exceptions import RoadEndError
from utils import hamming_distance, Pathfinder
from graph import GraphBuilder


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


class Grid:
    _paths: dict
    _encoder: BinaryEncoder
    graph_builder: GraphBuilder

    def create_graph_grid(self):
        self.graph_builder.make_graph_from_grid()

    def create_graph_path(self, translations: list[str], path: list[str]):
        path_2 = [
            f'{i + 1} | {path[i]}'
            for i in range(len(path))
        ]
        self.graph_builder.make_graph_encode(path=path_2, translations=translations)

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

                flag = False
                for path in paths_to_thread:
                    if self._paths[path][dibit] > min_difference or flag:
                        self._paths[path].pop(dibit)
                    else:
                        flag = True

    def __init__(self, encoder: tuple[str, str] | BinaryEncoder):

        if isinstance(encoder, BinaryEncoder):
            self._encoder = encoder
        else:
            self._encoder = BinaryEncoder(*encoder)

        self._paths = dict()
        self.create_grid()
        self.purge_grid()
        self.graph_builder = GraphBuilder(self)

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

    def encode(self, message: str) -> tuple[list[str], list[str]]:
        assert set(message) == {'0', '1'}

        result = list()
        vertex = '0' * (self._binary_encoder.k - 1)
        path = [vertex, ]
        for bit in message:
            result.append(self._binary_encoder.encode(f'{bit}{vertex}'))
            vertex = f'{bit}{vertex}'[:-1]
            path.append(vertex)

        return result, path

    def decode(self, encoded_message: list[str], maximum_depth: int) -> tuple[str, list[str]]:

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

            dibit = sequence[position]

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
                if path_metric < min_metric:
                    min_metric = path_metric
                    result = path[1]

            return result

        assert maximum_depth > 0
        result = ''
        vertex = '0' * (self._binary_encoder.k - 1)
        path = [vertex, ]
        for position in range(len(encoded_message)):
            vertex = find_next_step(
                vertex=vertex,
                sequence=encoded_message,
                position=position,
                maximum_depth=maximum_depth,
                grid=self._grid,
            )
            result = result + vertex[0]
            path.append(vertex)

        return result, path


if __name__ == "__main__":
    pass
