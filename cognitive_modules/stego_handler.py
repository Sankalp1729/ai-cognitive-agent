from PIL import Image

class StegoHandler:
    def embed_message(self, image_path, output_path, message):
        img = Image.new('RGB', (300, 100), color=(255, 255, 255))  # Create white image
        pixels = img.load()
        message_bits = ''.join(format(ord(c), '08b') for c in message)
        message_bits += '00000000'  # Null terminator

        idx = 0
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if idx < len(message_bits):
                    r, g, b = pixels[x, y]
                    r = (r & ~1) | int(message_bits[idx])
                    pixels[x, y] = (r, g, b)
                    idx += 1

        img.save(output_path)

    def extract_message(self, image_path):
        img = Image.open(image_path)
        pixels = img.load()
        bits = ""

        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b = pixels[x, y]
                bits += str(r & 1)

        chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
        message = ""
        for c in chars:
            char = chr(int(c, 2))
            if char == '\x00':  # Stop at null terminator
                break
            message += char
        return message

