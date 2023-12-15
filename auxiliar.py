import pygame as pg

class SurfaceManager:

    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False, scale: int = 1) -> list[pg.surface.Surface]:
        sprites_list = list()
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)

        for row in range(rows):
            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height
                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )
                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                if scale != 1:
                    frame_surface = pg.transform.scale_by(frame_surface, scale)
                sprites_list.append(frame_surface)
        return sprites_list