from dataclasses import dataclass
import os

path_base_default = os.getenv('ASTRO_IMAGING_DATA_PATH', default='./')


@dataclass
class Paths:
    base: str = path_base_default
    catalogs: str = None
    images: str = None

    def __post_init__(self):
        if self.catalogs is None:
            self.catalogs = os.path.join(self.base, 'catalogs')
        if self.images is None:
            self.images = os.path.join(self.base, 'images')


paths_default = Paths()
