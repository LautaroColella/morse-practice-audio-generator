from pydub import AudioSegment
import configparser
import os


def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    level = config.get("settings", "level")

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

    if level == "arbitrary":
        delay_between_sounds = config.getint(
            "settings", "arbitrary_delay_between_sounds"
        )
        delay_between_characters = config.getint(
            "settings", "arbitrary_delay_between_characters"
        )
        delay_between_words = config.getint("settings", "arbitrary_delay_between_words")

        sound_delay_map = {
            "delay_between_sounds": delay_between_sounds,
            "delay_between_characters": delay_between_characters,
            "delay_between_words": delay_between_words,
        }
    else:
        if level not in level_config_map:
            raise ValueError(
                f"Invalid level '{level}' in config file. Choose from: arbitrary, {', '.join(level_config_map.keys())}"
            )

        sound_delay_map = level_config_map[level]

    dot_sound_file = config.get("settings", "dot_sound_file")
    dash_sound_file = config.get("settings", "dash_sound_file")
    sound_map = {".": dot_sound_file, "-": dash_sound_file}

    output_file = config.get("settings", "output_file")

    word_separator = config.get("settings", "word_separator")

    bitrate = config.get("settings", "bitrate")

    return sound_delay_map, sound_map, output_file, word_separator, bitrate


def generate_audio(
    input_string,
    sound_delay_map,
    sound_map,
    output_file="morse_output.mp3",
    word_separator="/",
    bitrate="32k",
):

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
                    return

            combined += silence_between_letters
        if word != words[len(words) - 1]:
            combined += silence_between_words

    combined.export(output_file, format="mp3", bitrate=bitrate)

    print(f"Generated audio file: {output_file}")


if __name__ == "__main__":

    config_file = "config.cfg"

    sound_delay_map, sound_map, output_file, word_separator, bitrate = read_config(
        config_file
    )

    input_string = input(f"Enter text in morse code, separated by '{word_separator}': ")

    generate_audio(
        input_string, sound_delay_map, sound_map, output_file, word_separator, bitrate
    )
