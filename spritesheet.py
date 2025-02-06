import pygame


class SpriteSheet:
    def __init__(self, image_path, frame_width=148, frame_height=128):
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = self._extract_frames()
        self.current_frame = 0

    def _extract_frames(self):
        """Разрезает спрайт-лист на отдельные кадры."""
        sheet_width, sheet_height = self.sprite_sheet.get_size()
        frames = []
        for y in range(0, sheet_height, self.frame_height):
            for x in range(0, sheet_width, self.frame_width):
                frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                frames.append(frame)
        return frames

    def get_current_frame(self):
        """Возвращает текущий кадр."""
        return self.frames[self.current_frame]

    def next_frame(self):
        """Переключается на следующий кадр."""
        self.current_frame = (self.current_frame + 1) % len(self.frames)

    def set_frame(self, index):
        """Устанавливает текущий кадр по индексу."""
        if 0 <= index < len(self.frames):
            self.current_frame = index
