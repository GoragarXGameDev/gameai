class SceneManager:
    def __init__(self):
        self.loaded_scenes = []
        self.active_scene = None

    def add_scene(self, scene):
        self.loaded_scenes.append(scene)

    def set_active_scene(self, scene_name):
        for scene in self.loaded_scenes:
            if scene.name == scene_name:
                self.active_scene = scene
                return

        raise ValueError(f"No scene with name {scene_name} found")

scene_manager = SceneManager()

