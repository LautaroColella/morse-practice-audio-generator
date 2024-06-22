from pydub import AudioSegment
import configparser, re
from datetime import datetime


def read_config(file_path):
    level_config_map = {
        "beginner": {
            "delay_between_sounds": 3,
            "delay_between_characters": 5,
            "delay_between_words": 9,
        },
        "intermediate": {
            "delay_between_sounds": 1,
            "delay_between_characters": 5,
            "delay_between_words": 9,
        },
        "advanced": {
            "delay_between_sounds": 1,
            "delay_between_characters": 3,
            "delay_between_words": 7,
        },
    }

    formats_bitrate = {
        "mp3": ["32k", "64k", "96k", "128k", "192k", "256k", "320k"],
        "ogg": ["48k", "64k", "96k", "128k", "160k", "192k", "256k", "320k", "500k"],
        "wav": [],
        "flac": [],
    }

    config = configparser.ConfigParser()
    config.read(file_path)

    file_name = config.get("settings", "file_name", fallback="morse")
    file_format = config.get("settings", "file_format", fallback="mp3")
    use_curr_time = config.getint("settings", "use_current_time", fallback=1)
    bitrate = config.get("settings", "bitrate", fallback="32k")
    dot_sound_file = config.get("settings", "dot_sound_file", fallback="sounds/dot.mp3")
    dash_sound_file = config.get(
        "settings", "dash_sound_file", fallback="sounds/dash.mp3"
    )
    word_separator = config.get("settings", "word_separator", fallback="/")
    level = config.get("settings", "level", fallback="beginner")

    if word_separator in [" ", ".", "-"]:
        print(f"Unsupported word separator '{word_separator}' in config file")
        return {}, 1

    if not re.match("^[a-zA-Z0-9]+$", file_name):
        print(
            f"Unsupported file name '{file_name}' in config file. It can only contain alphanumeric characters"
        )
        return {}, 1

    if file_format not in formats_bitrate:
        print(
            f"Unsupported file format '{file_format}' in config file. Choose from: {', '.join(formats_bitrate.keys())}"
        )
        return {}, 1

    if (
        file_format not in ["wav", "flac"]
        and bitrate not in formats_bitrate[file_format]
    ):
        print(
            f"Unsupported bitrate '{bitrate}' for format '{file_format}' in config file. Choose from: {formats_bitrate[file_format]}"
        )
        return {}, 1

    if level == "arbitrary":
        delay_between_sounds = config.getint(
            "settings", "arbitrary_delay_between_sounds", fallback=3
        )
        delay_between_characters = config.getint(
            "settings", "arbitrary_delay_between_characters", fallback=5
        )
        delay_between_words = config.getint(
            "settings", "arbitrary_delay_between_words", fallback=9
        )

        sound_delay_map = {
            "delay_between_sounds": delay_between_sounds,
            "delay_between_characters": delay_between_characters,
            "delay_between_words": delay_between_words,
        }
    else:
        if level not in level_config_map:
            raise ValueError(
                f"Unsupported level '{level}' in config file. Choose from: arbitrary, {', '.join(level_config_map.keys())}"
            )

        sound_delay_map = level_config_map[level]

    sound_map = {".": dot_sound_file, "-": dash_sound_file}

    config_values = {
        "sound_delay_map": sound_delay_map,
        "sound_map": sound_map,
        "file_name": file_name,
        "file_format": file_format,
        "word_separator": word_separator,
        "bitrate": bitrate,
        "use_curr_time": use_curr_time,
    }

    return config_values, 0


def generate_audio(config_values, input_string):
    sound_delay_map = config_values["sound_delay_map"]
    sound_map = config_values["sound_map"]
    file_name = config_values["file_name"]
    file_format = config_values["file_format"]
    word_separator = config_values["word_separator"]
    bitrate = config_values["bitrate"]
    use_time = config_values["use_curr_time"]

    silence_between_parts = AudioSegment.silent(
        duration=len(sound_map["."]) * sound_delay_map["delay_between_sounds"] * 10
    )
    silence_between_letters = AudioSegment.silent(
        duration=len(sound_map["."]) * sound_delay_map["delay_between_characters"] * 10
    )
    silence_between_words = AudioSegment.silent(
        duration=len(sound_map["."]) * sound_delay_map["delay_between_words"] * 10
    )

    words = input_string.split(word_separator)
    combined = AudioSegment.empty()

    for word in words:
        letters = word.strip().split()
        for letter in letters:
            for character in letter:
                if character in sound_map:
                    sound = AudioSegment.from_mp3(sound_map[character])
                    combined += sound + silence_between_parts
                else:
                    print(f"Error: Invalid character '{character}'")
                    return 1

            combined += silence_between_letters
        if word != words[len(words) - 1]:
            combined += silence_between_words

    export_params = {"format": file_format}
    if file_format not in ["wav", "flac"]:
        export_params["bitrate"] = bitrate

    if use_time == 1:
        curr_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        output_name = f"{file_name}-{curr_time}.{file_format}"
    else:
        output_name = f"{file_name}.{file_format}"

    combined.export(output_name, **export_params)

    print(f"Generated audio file: '{output_name}'")

    return 0


if __name__ == "__main__":

    config_file = "config.cfg"
    config_values, config_error = read_config(config_file)

    if config_error == 0:
        input_string = input(f"Enter text in morse code: ")
        audio_error = generate_audio(config_values, input_string)
        if audio_error == 0:
            print("Press 'enter' to close")
        else:
            print("Press 'enter' to close")
            input()
    else:
        print("Press 'enter' to close")
        input()
