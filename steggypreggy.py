import argparse
import json
import random
import urllib.parse
from PIL import Image, ImageSequence

def fertilize_data(input_gif, output_gif, data_file):
    """Embed URL-encoded JSON data into a random frame of a GIF using LSB steganography."""
    with open(data_file, "rb") as file:
        raw_data = file.read().decode("utf-8", errors="ignore")

    encoded_data = urllib.parse.quote(raw_data)

    binary_data = "11111111" + format(len(encoded_data), '032b') + ''.join(format(ord(char), '08b') for char in encoded_data)
    data_index = 0

    gif = Image.open(input_gif)
    frames = []
    random_frame_index = random.randint(0, gif.n_frames - 1)

    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        frame = frame.convert("RGB")
        pixels = list(frame.getdata())
        new_pixels = []

        if i == random_frame_index:
            for pixel in pixels:
                r, g, b = pixel
                if data_index < len(binary_data):
                    r = (r & ~1) | int(binary_data[data_index])
                    data_index += 1
                new_pixels.append((r, g, b))
            new_frame = Image.new("RGB", frame.size)
            new_frame.putdata(new_pixels)
            frames.append(new_frame)
        else:
            frames.append(frame.copy())

    frames[0].save(output_gif, save_all=True, append_images=frames[1:], loop=gif.info.get("loop", 0), duration=gif.info.get("duration", 100))
    print(f"🥚 Gif Fertilized in frame {random_frame_index} of {output_gif}")

def harvest_data(input_gif):
    """Harvest URL-encoded JSON data from a GIF and properly decode it before saving."""
    gif = Image.open(input_gif)

    for i, frame in enumerate(ImageSequence.Iterator(gif)):
        frame = frame.convert("RGB")
        binary_data = ""
        pixels = list(frame.getdata())

        for pixel in pixels:
            r, _, _ = pixel
            binary_data += str(r & 1)

        if binary_data.startswith("11111111"):
            try:
                data_length = int(binary_data[8:40], 2)
                encoded_data = binary_data[40:40 + (data_length * 8)]
                decoded_data = "".join(chr(int(encoded_data[j:j + 8], 2)) for j in range(0, len(encoded_data), 8))

                harvested_json = urllib.parse.unquote(decoded_data)

                try:
                    json_data = json.loads(harvested_json)
                    output_file = "harvested_data.json"
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=4, ensure_ascii=False)
                    print(f"🐣 harvested data successfully to {output_file}")
                    return json_data
                except json.JSONDecodeError as e:
                    print(f"💩 JSON decoding failed: {e}")
                    return None

            except (ValueError, json.JSONDecodeError):
                continue

    print("💩 No data found in any frame.")
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SteggyPreggy - Make your gif datapreggers!")

    parser.add_argument("-e", "--embed", help="Fertilize your gif with data", action="store_true")
    parser.add_argument("-d", "--decode", help="Harvest data from a GIF", action="store_true")
    parser.add_argument("-i", "--input", help="Input JSON file", required=True)
    parser.add_argument("-f", "--file", help="Input GIF file to pregger")
    parser.add_argument("-o", "--output", help="Output GIF file (default: skelly_crypt.gif)", default="skelly_crypt.gif")

    args = parser.parse_args()

    if args.embed:
        if not args.file:
            print("💩 Error: You must specify a GIF file with `-f` when fertilizing.")
        else:
            fertilize_data(args.file, args.output, args.input)

    elif args.decode:
        harvest_data(args.input)

    else:
        print("💩 Error: You must specify either `-e` for fertilizing or `-d` for harvesting.")
        parser.print_help()