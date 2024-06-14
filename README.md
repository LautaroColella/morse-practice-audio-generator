# Morse Code Audio Generator

This Python program generates an audio file (.mp3) from morse code text input based on specified configurations.

## Installation

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Install dependencies:**

    ```sh
    pip install pydub
    ```

    **IMPORTANT**: `pydub` requires ffmpeg to work, you have to [install it from the oficial website](https://ffmpeg.org/) and add it to your `PATH`.

3. **Prepare configuration:**

    Create or modify `config.cfg` file according to your preferences. See [Configuration Details](#configuration-details) below for more information.

## Usage

1. **Run the program:**

    ```sh
    python morse_code_generator.py
    ```

2. **Enter text input:**

    Enter the Morse code text you wish to convert to audio, separated by the specified word separator (default is "/").

3. **Output:**

    The program will generate an audio file (`morse_output.mp3`) in the same directory.

## Configuration Details

The `config.cfg` file allows customization for Morse code audio generation

- `dot_sound_file`: Path to the sound file for a dot.
- `dash_sound_file`: Path to the sound file for a dash.
- `output_file`: Path where the generated audio file will be saved.
- `word_separator`: Separator used to split words in the input.
- `level`: Specifies the Morse code timing level.

**Level Settings:**

- **beginner:** Suitable for beginners, with longer pauses.
- **intermediate:** Uses Farnsworth Timing.
- **advanced:** Standard Morse code timing.
- **arbitrary:** Define custom delays

For "arbitrary" level:

- `arbitrary_delay_between_sounds`: Custom delay between sounds (`--.` is `- %DELAY% -.`)
- `arbitrary_delay_between_characters`: Custom delay between characters (`- -.` is `- %DELAY% -.`)
- `arbitrary_delay_between_words`: Custom delay between words. (`--. - / -.` is `--. - %DELAY% -.`)

## Example Configuration

```ini
[settings]
dot_sound_file = sounds/dot.mp3
dash_sound_file = sounds/dash.mp3
output_file = morse_output.mp3
word_separator = /
level = beginner

arbitrary_delay_between_sounds = 9
arbitrary_delay_between_characters = 9
arbitrary_delay_between_words = 9
```

## LICENSE

MIT License

Copyright (c) 2024 Lautaro Colella

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
