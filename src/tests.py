import unittest
from encoder import Grid, BinaryEncoder, Encoder


class TestBinaryEncoder(unittest.TestCase):
    def test_encoder_init_1(self):
        encoder = BinaryEncoder('100', '111')
        self.assertEqual(
            (
                [0],
                [0, 1, 2],
            ),
            (
                encoder._upper,
                encoder._lower
            )
        )

    def test_encoder_1(self):
        encoder = BinaryEncoder('100', '111')
        self.assertEqual(
            [
                '00',
                '01',
                '01',
                '00',
                '11',
                '10',
                '10',
                '11'
            ],
            [
                encoder.encode('{0:03b}'.format(i))
                for i in range(8)
            ]
        )


class TestGrid(unittest.TestCase):
    def test_easy_grid_creation_1(self):
        grid = Grid(encoder=('100', '111'))
        self.assertEqual(
            {
                ('00', '00'): {'00': 0, '10': 1},
                ('00', '10'): {'01': 1, '11': 0},
                ('01', '00'): {'01': 0, '11': 1},
                ('01', '10'): {'00': 1, '10': 0},
                ('10', '01'): {'01': 0, '11': 1},
                ('10', '11'): {'00': 1, '10': 0},
                ('11', '01'): {'00': 0, '10': 1},
                ('11', '11'): {'01': 1, '11': 0}
            },
            grid.paths
        )

    def test_grid_creation_1(self):
        grid = Grid(encoder=('101', '111'))
        self.assertEqual(
            {('00', '00'): {'00': 0, '01': 1, '10': 1},
             ('00', '10'): {'01': 1, '10': 1, '11': 0},
             ('01', '00'): {'11': 0},
             ('01', '10'): {'00': 0},
             ('10', '01'): {'00': 1, '01': 0, '11': 1},
             ('10', '11'): {'00': 1, '10': 0, '11': 1},
             ('11', '01'): {'10': 0},
             ('11', '11'): {'01': 0}},
            grid.paths
        )

    def test_grid_creation_2(self):
        grid = Grid(encoder=('1101', '1111'))
        self.assertEqual(
            {('000', '000'): {'00': 0, '01': 1, '10': 1},
             ('000', '100'): {'01': 1, '10': 1, '11': 0},
             ('001', '000'): {'11': 0},
             ('001', '100'): {'00': 0},
             ('010', '001'): {'00': 1, '01': 0, '11': 1},
             ('010', '101'): {'00': 1, '10': 0, '11': 1},
             ('011', '001'): {'10': 0},
             ('011', '101'): {'01': 0},
             ('100', '010'): {'01': 1, '10': 1, '11': 0},
             ('100', '110'): {'00': 0, '01': 1, '10': 1},
             ('101', '010'): {'00': 0},
             ('101', '110'): {'11': 0},
             ('110', '011'): {'00': 1, '10': 0, '11': 1},
             ('110', '111'): {'00': 1, '01': 0, '11': 1},
             ('111', '011'): {'01': 0},
             ('111', '111'): {'10': 0}},
            grid.paths
        )


class TestEncoder(unittest.TestCase):
    def test_encode_1(self):
        encoder = Encoder(encoder=('1101', '1111'))
        self.assertEqual(
            ['11', '11', '10', '00'],
            encoder.encode('1010')[0]
        )

    def test_decode_1(self):
        encoder = Encoder(encoder=('1101', '1111'))
        self.assertEqual(
            '1010',
            encoder.decode(['11', '11', '10', '00'], 4)[0]
        )

    def test_encode_2E(self):
        encoder = Encoder(encoder=('1101101', '1001111'))
        self.assertEqual(
            ['11', '10', '00', '00', '01', '10', '10', '00', '11'],
            encoder.encode('100101011')[0]
        )

    def test_decode_2E(self):
        encoder = Encoder(encoder=('1101101', '1001111'))
        self.assertEqual(
            '100101011',
            encoder.decode(['11', '10', '00', '00', '01', '10', '10', '00', '11'], maximum_depth=8)[0]
        )


if __name__ == '__main__':
    unittest.main()
