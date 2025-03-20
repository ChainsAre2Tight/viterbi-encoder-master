# Convolutional Encoder CLI

## Overview
This CLI program implements **convolutional encoding** and **Viterbi decoding** for error correction. It supports encoding, decoding, and generating a graphical visualization of the encoding process.

## Features
- **Encode** binary strings using convolutional encoding
- **Decode** encoded binary data using the Viterbi algorithm
- **Generate an HTML visualization** of the encoding grid

## Installation (Linux)
1. **Install Python 3.12** (if not installed):
   ```bash
   sudo apt update && sudo apt install python3.12 python3.12-venv python3.12-dev
   ```
2. **Clone this repository:**
   ```bash
   git clone https://github.com/ChainsAre2Tight/viterbi-encoder-master
   cd viterbi-encoder-master
   ```
3. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the program from the command line with the following options:

### **Encoding**
```bash
python main.py --task encode --input <binary_string>
```
Example:
```bash
python main.py --task encode --input 1101
```
(Default encoder: `101 111`)

### **Decoding**
```bash
python main.py --task decode --input <encoded_binary_string> [--depth <max_search_distance>]
```
Example:
```bash
python main.py --task decode --input 101101 --depth 8
```
(Default maximum search distance: `8`)

### **Graph Visualization**
```bash
python main.py --task draw_graph [--graph <output_filename>]
```
Example:
```bash
python main.py --task draw_graph --graph encoding_visualization
```
(Default filename: `result.html`)

## Arguments
| Argument        | Description |
|----------------|-------------|
| `--task` (`-t`) | Task to execute: `encode`, `decode`, or `draw_graph` (required) |
| `--input` (`-i`) | Input binary string (required for encoding/decoding) |
| `--encoder` (`-e`) | Binary encoder specification, e.g., `"101 111"` (optional, default: `101 111`) |
| `--depth` (`-d`) | Maximum search depth for decoding (optional, default: `8`) |
| `--graph` (`-g`) | Output filename for saving graph visualization (optional) |

## Example Output
- Encoding `1101` → `101101`
- Decoding `101101` → `1101`
- Generates `encoding_visualization.html` with a graphical representation

## Dependencies
- Python 3.12
- Required dependencies are listed in `requirements.txt`

## Contributing
Feel free to submit issues or pull requests to improve this project.

## License
This project is licensed under the MIT License.

