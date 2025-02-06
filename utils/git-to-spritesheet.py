import os
from PIL import Image, ImageSequence


def interpolate_frames(frame1, frame2, alpha):
    """Интерполяция между двумя кадрами."""
    return Image.blend(frame1, frame2, alpha)


def gif_to_spritesheet(input_folder, output_folder, frame_size=(148, 128), num_frames=60):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".gif"):
            gif_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")

            with Image.open(gif_path) as img:
                frames = [frame.copy().convert("RGBA").resize(frame_size) for frame in ImageSequence.Iterator(img)]

                if len(frames) > num_frames:
                    # Создаем промежуточные кадры
                    new_frames = []
                    step = (len(frames) - 1) / (num_frames - 1)
                    for i in range(num_frames):
                        idx = i * step
                        idx1 = int(idx)
                        idx2 = min(idx1 + 1, len(frames) - 1)
                        alpha = idx - idx1
                        new_frame = interpolate_frames(frames[idx1], frames[idx2], alpha)
                        new_frames.append(new_frame)
                    frames = new_frames
                else:
                    frames = frames[:num_frames] + [frames[-1]] * max(0, num_frames - len(frames))

                spritesheet_width = frame_size[0] * num_frames
                spritesheet_height = frame_size[1]
                spritesheet = Image.new("RGBA", (spritesheet_width, spritesheet_height))

                for i, frame in enumerate(frames):
                    spritesheet.paste(frame, (i * frame_size[0], 0))

                spritesheet.save(output_path)
                print(f"Saved: {output_path}")


# Использование
input_directory = "D:\Work-space\Projects\Dice-Dungeon\Assets\Graphics\enemies"  # Папка с GIF файлами
output_directory = "../Assets/Graphics/spritesheets"  # Папка для спрайт-листов
gif_to_spritesheet(input_directory, output_directory)