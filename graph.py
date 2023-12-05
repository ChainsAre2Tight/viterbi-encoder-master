from encoder import Grid, BinaryEncoder
import pyvis


class GraphBuilder:
    vertex_color = 'red'
    vertex_shape = 'dot'
    background_color = 'white'
    horizontal_offset = 300
    vertical_offset = 100
    _graph: pyvis.network.Network
    _grid: Grid

    def __init__(self, grid: Grid):
        self._graph = pyvis.network.Network(notebook=True, directed=True, bgcolor=self.background_color)
        self._graph.toggle_physics(False)

        self._grid = grid

    def _add_column(self, vertices: tuple[str], column_index: int):
        X = self.horizontal_offset * column_index
        for index, vertex in enumerate(vertices):
            Y = self.vertical_offset * index
            self._graph.add_node(
                n_id=f'{column_index + 1} | {vertex}',
                color=self.vertex_color,
                shape=self.vertex_shape,
                x=X,
                y=Y,
            )

    def _add_translations(self, dibit: str, index: int):
        assert 0 <= index < 4
        assert dibit in ('00', '01', '10', '11')

        for key, value in self._grid.paths.items():
            title = 'error'
            for name, v in value.items():
                if v == 0:
                    title = name
            print(value.keys())
            if dibit in value.keys():
                print(
                    f'{index + 1} | {key[0]}',
                    f'{index + 2} | {key[1]}',
                    f'{title} ({value[dibit]})',
                    sep='-------'
                )
                self._graph.add_edge(
                    f'{index + 1} | {key[0]}',
                    f'{index + 2} | {key[1]}',
                    title=f'{title} ({value[dibit]})'
                )

    def make_graph(self):

        # make 2-dimensional array of vertices to address them later
        # X - index of column
        # Y - index of vertex within its column

        nodes: tuple[str] = tuple(
            '{0:02b}'.format(i)
            for i in range(2 ** (self._grid._encoder.k - 1))
        )

        possible_translations = ('00', '01', '10', '11')

        vertices = [
            nodes
            for _ in range(len(possible_translations) + 1)
        ]

        # place translations above
        Y = -(self.vertical_offset)
        for index, translation in enumerate(possible_translations):
            X = (self.horizontal_offset // 2) + self.horizontal_offset * index
            self._graph.add_node(translation, x=X, y=Y, shape=self.vertex_shape, color=self.background_color)

        # place columns
        for index, column in enumerate(vertices):
            self._add_column(column_index=index, vertices=column)

        # place edges
        for index, dibit in enumerate(possible_translations):
            self._add_translations(dibit=dibit, index=index)

        # export
        self._graph.show('result.html')


class TestGrid(Grid):

    def create_graph(self):
        graphbuilder = GraphBuilder(self)
        graphbuilder.make_graph()

    def __init__(self, encoder: tuple[str, str] | BinaryEncoder):
        super().__init__(encoder)
        self.create_graph()


if __name__ == "__main__":
    testgrid = TestGrid(encoder=('101', '111'))
