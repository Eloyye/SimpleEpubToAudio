# SimpleEpubToAudio
## Overview
Simple program to convert epub files to audio using xtts

## Usage
1. In cwd, install the necessary dependencies:
```bash
conda env create -f environment.yml
```
2. Run python script
```bash
python src/main.py <path-to-epub-file>
```
3. Install xtts model when prompted
4. Output file should be in `output/combined_audio/`
