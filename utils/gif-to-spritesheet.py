from PIL import Image
import os


def extract_frames(gif_path):
    """Извлекает кадры из GIF и возвращает их списком."""
    frames = []
    with Image.open(gif_path) as img:
        for frame in range(img.n_frames):
            img.seek(frame)
            frames.append(img.copy().convert("RGBA"))
    return frames


def create_spritesheet(frames, output_path):
    """Создает spritesheet из списка кадров и сохраняет его."""
    if not frames:
        return

    frame_width, frame_height = frames[0].size
    sheet_width = frame_width * len(frames)
    sheet_height = frame_height

    spritesheet = Image.new("RGBA", (sheet_width, sheet_height))

    for i, frame in enumerate(frames):
        spritesheet.paste(frame, (i * frame_width, 0))

    spritesheet.save(output_path)


def process_gifs_in_directory(input_dir, output_dir):
    """Обрабатывает все GIF-файлы в каталоге."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".gif"):
            gif_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + "_spritesheet.png")

            frames = extract_frames(gif_path)
            create_spritesheet(frames, output_path)
            print(f"Создан спрайт-лист: {output_path}")


if __name__ == "__main__":
    input_directory = ""  # Укажите каталог с GIF-файлами
    output_directory = "spritesheets"  # Укажите каталог для сохранения спрайт-листов
    process_gifs_in_directory(input_directory, output_directory)
