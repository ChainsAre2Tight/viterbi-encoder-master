import pyvis


class GraphBuilder:
    vertex_color = 'gray'
    edge_color = 'black'
    highlight_color_primary = 'red'
    vertex_shape = 'dot'
    background_color = 'white'
    horizontal_offset = 300
    vertical_offset = 100
    _graph: pyvis.network.Network

    def __init__(self, grid):
        self._graph = pyvis.network.Network(notebook=True, directed=True, bgcolor=self.background_color, height=1000,
                                            width=1920)
        self._graph.toggle_physics(False)

        self._grid = grid

    def _add_column(self, vertices: tuple[str], column_index: int, highlight_nodes: list[str]):
        X = self.horizontal_offset * column_index
        for index, vertex in enumerate(vertices):
            Y = self.vertical_offset * index
            node = f'{column_index + 1} | {vertex}'
            self._graph.add_node(
                n_id=node,
                color=self.highlight_color_primary if node in highlight_nodes else self.vertex_color,
                shape=self.vertex_shape,
                x=X,
                y=Y,
            )

    def _add_translations(self, dibit: str, index: int, highlight_edges: list[tuple[str, str]] | None = None):
        assert dibit in ('00', '01', '10', '11')
        if highlight_edges is None:
            highlight_edges = []

        for key, value in self._grid.paths.items():
            title = 'error'
            for name, v in value.items():
                if v == 0:
                    title = name
            if dibit in value.keys():

                edge = (f'{index + 1} | {key[0]}', f'{index + 2} | {key[1]}')
                self._graph.add_edge(
                    edge[0], edge[1],
                    title=f'{title} ({value[dibit]})',
                    color=self.highlight_color_primary if edge in highlight_edges else self.edge_color
                )

    def make_graph(self, translations, highlight_nodes: list[str] | None = None):
        if highlight_nodes is None:
            highlight_nodes = list()

        # make 2-dimensional array of vertices to address them later
        # X - index of column
        # Y - index of vertex within its column
        format = '{0:0' + str(self._grid._encoder.k - 1) + 'b}'

        nodes: tuple[str] = tuple(
            format.format(i)
            for i in range(2 ** (self._grid._encoder.k - 1))
        )

        vertices = [
            nodes
            for _ in range(len(translations) + 1)
        ]

        # place translations above
        Y = -(self.vertical_offset)
        for index, translation in enumerate(translations):
            X = (self.horizontal_offset // 2) + self.horizontal_offset * index
            self._graph.add_node(f'{index + 1} | {translation}', x=X, y=Y, shape=self.vertex_shape, color=self.background_color)

        # place columns
        for index, column in enumerate(vertices):
            self._add_column(column_index=index, vertices=column, highlight_nodes=highlight_nodes)

        # place edges
        path_2 = [
            (highlight_nodes[i], highlight_nodes[i + 1])
            for i in range(len(highlight_nodes) - 1)
        ]
        for index, dibit in enumerate(translations):
            self._add_translations(dibit=dibit, index=index, highlight_edges=path_2)

        # export
        self._graph.show('result.html')

    def make_graph_encode(self, translations: list[str] | tuple[str], path: list[str]):
        self.make_graph(translations=translations, highlight_nodes=path)

    def make_graph_from_grid(self):
        self.make_graph(translations=('00', '01', '10', '11'))
