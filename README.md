# outputLinkParser
Designed for making sense of CICADA FPGA output link dumps
## Setup
```
python3 -m venv outputLinkEnv
source outputLinkEnv/bin/activate
python3 -m pip install rich
```

### Running & Options
The script itself is under `parseOutputLinks.py`, and it takes three possible arguments, with one required.
- `-f` or `--fileName`: This is required, and should be the path to the file that is being dumped into the table. Only one argument at a time accepted
- `--headerLines`: Number of lines at the top of the file describing things that are not link contents. This is used to discard those lines
- `--skipLines` or `-s`: Number of link lines at the start of the event to skip. this is used to skip to the first complete event in case the output dump is offset by incomplete caloSummary events.