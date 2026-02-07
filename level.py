import random

TILE_SIZE = 48 

TERRAIN_DIRT = 0
TERRAIN_GRASS = 1
TERRAIN_DARK_GRASS = 2

class Level:
    def __init__(self):
        self.cols = 50
        self.rows = 50
        
        self.width_px = self.cols * TILE_SIZE
        self.height_px = self.rows * TILE_SIZE
        
        self.grid = []
        self.visual_variations = []
        
        self._generate_map()

    def _generate_map(self):
        self.grid = [[TERRAIN_DIRT for _ in range(self.cols)] for _ in range(self.rows)]
        self.visual_variations = [[0.0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        for y in range(self.rows):
            for x in range(self.cols):
                self.visual_variations[y][x] = random.random()

        for _ in range(40):
            w = random.randint(4, 12)
            h = random.randint(4, 12)
            start_x = random.randint(1, self.cols - w - 1)
            start_y = random.randint(1, self.rows - h - 1)
            
            for y in range(start_y, start_y + h):
                for x in range(start_x, start_x + w):
                    if 0 <= y < self.rows and 0 <= x < self.cols:
                        self.grid[y][x] = TERRAIN_GRASS

        num_dark_patches = 20
        for _ in range(num_dark_patches):
            w = random.randint(2, 5)
            h = random.randint(2, 5)
            start_x = random.randint(1, self.cols - w - 1)
            start_y = random.randint(1, self.rows - h - 1)
            
            can_place = True
            for y in range(start_y, start_y + h):
                for x in range(start_x, start_x + w):
                    if 0 <= y < self.rows and 0 <= x < self.cols:
                        if self.grid[y][x] == TERRAIN_DIRT:
                            can_place = False
                    else:
                        can_place = False
            
            if can_place:
                for y in range(start_y, start_y + h):
                    for x in range(start_x, start_x + w):
                        self.grid[y][x] = TERRAIN_DARK_GRASS

    def _get_tile_name(self, id_num):
        return f"tile_{id_num:03d}"

    def draw(self, screen, images, camera_x, camera_y):
        screen_w = screen.surface.get_width()
        screen_h = screen.surface.get_height()
        padding = 2
        
        start_col = max(0, int(camera_x // TILE_SIZE))
        end_col = min(self.cols, int((camera_x + screen_w) // TILE_SIZE) + padding)
        start_row = max(0, int(camera_y // TILE_SIZE))
        end_row = min(self.rows, int((camera_y + screen_h) // TILE_SIZE) + padding)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE
                screen_x = world_x - camera_x
                screen_y = world_y - camera_y
                
                dirt_id = 6 
                rnd = self.visual_variations[y][x]
                if rnd > 0.90: dirt_id = 7
                elif rnd > 0.80: dirt_id = 14
                elif rnd > 0.70: dirt_id = 15
                elif rnd > 0.60: dirt_id = 22
                elif rnd > 0.50: dirt_id = 23
                
                tile_name = self._get_tile_name(dirt_id)
                screen.blit(getattr(images.tiles.dirt, tile_name), (screen_x, screen_y))
                
                cell_type = self.grid[y][x]
                if cell_type == TERRAIN_GRASS or cell_type == TERRAIN_DARK_GRASS:
                    self._draw_grass(screen, images, x, y, screen_x, screen_y, cell_type)

    def _draw_grass(self, screen, images, x, y, screen_x, screen_y, cell_type):
        
        n = self.grid[y-1][x] if y > 0 else TERRAIN_GRASS
        s = self.grid[y+1][x] if y < self.rows - 1 else TERRAIN_GRASS
        w = self.grid[y][x-1] if x > 0 else TERRAIN_GRASS
        e = self.grid[y][x+1] if x < self.cols - 1 else TERRAIN_GRASS

        is_dirt_n = (n == TERRAIN_DIRT)
        is_dirt_s = (s == TERRAIN_DIRT)
        is_dirt_w = (w == TERRAIN_DIRT)
        is_dirt_e = (e == TERRAIN_DIRT)

        base_tile_id = None
        base_folder = images.tiles.grass_border

        if is_dirt_n:
            base_tile_id = 0 if is_dirt_w else (2 if is_dirt_e else 1)
        elif is_dirt_s:
            base_tile_id = 16 if is_dirt_w else (18 if is_dirt_e else 17)
        elif is_dirt_w: base_tile_id = 8
        elif is_dirt_e: base_tile_id = 10
        else:
            base_folder = images.tiles.grass
            base_tile_id = 9
            if cell_type == TERRAIN_GRASS:
                rnd = self.visual_variations[y][x]
                if rnd > 0.90: base_tile_id = 5
                elif rnd > 0.80: base_tile_id = 13
                elif rnd > 0.70: base_tile_id = 21

        if base_tile_id is not None:
            tile_name = self._get_tile_name(base_tile_id)
            screen.blit(getattr(base_folder, tile_name), (screen_x, screen_y))

        if cell_type == TERRAIN_DARK_GRASS:
            self._draw_dark_grass_overlay(screen, images, x, y, screen_x, screen_y)

    def _draw_dark_grass_overlay(self, screen, images, x, y, screen_x, screen_y):
        
        def is_dark(gy, gx):
            if 0 <= gy < self.rows and 0 <= gx < self.cols:
                return self.grid[gy][gx] == TERRAIN_DARK_GRASS
            return False 

        n_is_dark = is_dark(y-1, x)
        s_is_dark = is_dark(y+1, x)
        w_is_dark = is_dark(y, x-1)
        e_is_dark = is_dark(y, x+1)

        tile_id = 33 # Centro padrão (meio)

        if not n_is_dark:
            if not w_is_dark: tile_id = 24  # Canto Sup Esq
            elif not e_is_dark: tile_id = 26 # Canto Sup Dir
            else: tile_id = 25              # Topo Centro
        # Baixo
        elif not s_is_dark:
            if not w_is_dark: tile_id = 39  # Canto Inf Esq
            elif not e_is_dark: tile_id = 41 # Canto Inf Dir
            else: tile_id = 40              # Baixo Centro
        # Laterais (Meio)
        elif not w_is_dark:
            tile_id = 32 # Esquerda
        elif not e_is_dark:
            tile_id = 34 # Direita
        else:
            tile_id = 33 # Centro 

        tile_name = self._get_tile_name(tile_id)
        screen.blit(getattr(images.tiles.grass_dark, tile_name), (screen_x, screen_y))

