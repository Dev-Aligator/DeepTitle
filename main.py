#!/usr/bin/env python
from models import Line
from translate import Translator
import argparse 

def get_argument():
    encoding_choices = {
        'utf-8': 'UTF-8 (Unicode Transformation Format 8-bit)',
        'utf-16': 'UTF-16 (Unicode Transformation Format 16-bit)',
        'utf-16le': 'UTF-16 Little-Endian',
        'utf-16be': 'UTF-16 Big-Endian',
        'iso-8859-1': 'ISO 8859-1 (Latin-1)',
        'iso-8859-2': 'ISO 8859-2 (Latin-2)',
        'windows-1252': 'Windows-1252 (Windows Western European)',
    }    
    parser = argparse.ArgumentParser(description='DeepTitle - An automatic subtitle translator')
    
    # Positional argument(s)
    parser.add_argument('originalFileName', metavar="originalfile", type=str, help='The SubRip text file you want to translate')
    
    # Optional argument(s)
    parser.add_argument('-e', '--email', type=str, help='Translated.com valid user email for more chars/day', metavar="", default="")
    parser.add_argument('-s', '--source', type=str, help="The original language", default="en", metavar="")
    parser.add_argument('-d', '--dist', type=str, help="The desired language", default="vi", metavar="")
    parser.add_argument('--encode', type=str, help='The Character Encoding technique that matches your file. Allowed values are: ' +', '.join(encoding_choices.keys()), default="utf-16", metavar="", choices=encoding_choices.keys())
    
    args = parser.parse_args()
    
    arguments = {
        'originalFileName': args.originalFileName,
        'email': args.email,
        'source': args.source,
        'dist': args.dist,
        'encode': args.encode
    }

    return arguments


def read_srt_file(filename, encode="utf-8-sig"):
    lines = []
    with open(filename, 'r', encoding=encode) as file:  # Specify the encoding
        srt_data = file.read().strip().split('\n\n')
        for block in srt_data:
            parts = block.split('\n')
            if len(parts) >= 3:
                # Strip leading whitespace and BOM character (\ufeff) from ID
                id = int(parts[0].lstrip('\ufeff'))
                time_parts = parts[1].split(' --> ')
                startTime = time_parts[0]
                endTime = time_parts[1]
                scripts = '\n'.join(parts[2:])
                lines.append(Line(id, startTime, endTime, scripts))
    return lines


def write_srt_file(filename, lines: list[Line]):
    with open(filename, 'w') as file:  # Specify the encoding
        for line in lines:
            file.write(str(line.id) + "\n" + line.startTime + " --> " + line.endTime + "\n" + line.scripts + "\n\n")

def translate_lines(lines: list[Line], chunk_size = 500):
    dialog = ""
    startChunk = 0
    for line_index in range(len(lines)):
        if len(dialog + lines[line_index].scripts) + 4 < chunk_size:
            dialog += lines[line_index].scripts + f"[*]"
        else:
            translated_dialog_raw = translator.translate(dialog)
            translated_scripts = translated_dialog_raw.split("[*]")
            translated_scripts = [s.strip() for s in translated_scripts if s.strip()]
            # print((translated_scripts))
            index = 0
            for prev_line_index in range(startChunk, line_index):
                try:
                    # print(index, lines[prev_line_index].scripts, "|", translated_scripts[index])
                    lines[prev_line_index].scripts = translated_scripts[index]
                    index += 1
                except:
                    # print(index, lines[prev_line_index].scripts, translated_scripts[index-1])
                    print(dialog)
                    print(translated_dialog_raw)
                    print(len(translated_scripts))
                    print(line_index - startChunk)
            startChunk = line_index
            print(startChunk)
            dialog = lines[line_index].scripts + "[*]"
    return lines
# Specify the path to your SRT file

# Call the read_srt_file function to get a list of Line objects
if __name__ == "__main__":
    system_arguments = get_argument()
    srt_original_filename = system_arguments['originalFileName']
    translator= Translator(from_lang=system_arguments['source'], to_lang=system_arguments['dist'], email=system_arguments['email'])
    lines_original = read_srt_file(srt_original_filename, encode=system_arguments['encode'])
    lines_dist = translate_lines(lines_original)
    write_srt_file("result.srt", lines_dist)
