from encoder import Encoder, BinaryEncoder, Grid
from exceptions import BadArgumentError

import sys
import argparse

default_encoder_args = '101 111'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Performs encoding and decoding tasks')
    parser.add_argument('-t', '--task', help='Task to execute. Can be either "encode", "decode", "draw_graph"',
                        required=True)
    parser.add_argument('-e', '--encoder',
                        help='Binary encoder options. Expected two binary numbers of the same length that make up the \
                        binary encoder. Example (and default values) "101 111"',
                        required=False)
    parser.add_argument('-i', '--input',
                        help='Input for program. Graph drawing doesnt require any input, enode and decode expect a binary string',
                        required=False)
    parser.add_argument('-d', '--depth',
                        help='Maximum search distance for decoding. Default is 8',
                        required=False)

    args = vars(parser.parse_args())

    # validate task
    task = args['task']
    if task not in ('draw_graph', 'encode', 'decode'):
        raise BadArgumentError(f'Unexpected task "{task}". See --help')
    else:
        print('Task is valid')

    # validate encoder
    encoder_args = args['encoder']
    if encoder_args is None:
        encoder_args = default_encoder_args
        print('Encoder is not specified. Using default values')
    elif len(encoder_args.split(' ')) != 2 or type(encoder_args) != str or not set(encoder_args).issubset(
            {'0', '1', ' '}):
        raise BadArgumentError('Expected two binary numbers for encoder args. See --help')
    else:
        print('Encoder args are valid')

    binary_encoder = BinaryEncoder(*encoder_args.split(' '))

    input_args = args['input']
    # validate input
    match task:
        case 'draw_graph':
            pass
        case 'encode':
            if not set(input_args).issubset({"0", "1"}):
                raise BadArgumentError('Expected to get binary string for "encode" task')
            else:
                print('Valid input')
        case 'decode':
            if not set(input_args).issubset({"0", "1"}) and len(input_args) % 2 == 0:
                raise BadArgumentError('Expected to get binary string for "decode" task whose length is divisible by 2')
            else:
                print('Valid input')

    # validate maximum depth argument
    depth_arg = None
    if task == 'decode':
        if args['depth'] is not None:
            depth_arg = int(args['depth'])
            print('Maximum search distance is set to', depth_arg)
        else:
            depth_arg = 8
            print(f'Maximum search distance is set to 8 (default)')

    match task:
        case 'draw_graph':
            print('Drawing graph...')
            grid = Grid(encoder=binary_encoder)
            grid.create_graph()
            print('Successful')

        case 'encode':
            print('Encoding message...')
            encoder = Encoder(encoder=binary_encoder)
            result = encoder.encode(input_args)
            print('Result:', ''.join(result))
            print('Successful')

        case 'decode':
            print('Decoding message...')
            encoder = Encoder(encoder=binary_encoder)
            message_to_decode = [
                input_args[i:i+2]
                for i in range(0, len(input_args), 2)
            ]
            result = encoder.decode(message_to_decode, maximum_depth=depth_arg)
            print('Result:', result)
            print('Successful')
