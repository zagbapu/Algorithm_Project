import zarr
import pandas as pd, numpy as np
import itertools as it # I will be using the `itertools.chain` function
from pathlib import Path # for better file/path operations management

# z1 = zarr.open('Lyft sampledataset/sample.zarr', mode='w', shape=(10000, 10000), chunks=(1000, 1000), dtype='i4')
# z1

# =====================================================================
# Global Variable/s

#1: Root of dataset:
DATA_ROOT = Path('Lyft sampledataset/sample.zarr')



# =====================================================================
# FUNCTIONS:
# FUN1: scene extraction
def parse_scene(scene):
    scene_dict = {
        "frame_index_interval_start": scene[0][0],
        "frame_index_interval_end": scene[0][1],
        "host": scene[1],
        "start_time": scene[2],
        "end_time": scene[3]
    }
    return scene_dict




# DATASET DEFINITION :
#1: The whole dataset
zl5 = zarr.open(DATA_ROOT.as_posix(), mode="r")
zl5

#2: SCENES:
zScenes = zarr.open(DATA_ROOT.joinpath("scenes").as_posix(), mode="r")
zScenes

# General Info about Dataset
print('Dataset General Info \n', zl5.info)
""" The dataset name is obivously equal to "/" as we're in the root folder. The has 5 memebers, namely:
        Scenes : a collection of frames
        Frames : a collection of agents (the host agents + other agents)
        Agents : Any object in circulation with the automatic vehicle (AV)
        Traffic_light_faces : traffic lights and their faces (bulbs)
"""

# Detailed Tree of Dataset
print('Detailed Tree', zl5.tree(expand=True))
""" So there are:

    100 scenes in the sample dataset
    24838 frames
    1893736 agents
    316008 traffic_light_faces
"""

# Info from Scene
print('SCENE\n', zl5.scenes.info)

# Scene data type
print('SCENE DATATYPE: \n', zl5.scenes.dtype)

"""A scene consists of 3 block of things :

    Frames : a scene has a list of frames that start from scene.frame_index_interval[0] and ends at scene.frame_index_interval[1]
    Host : a scene has a host which is the AV that films the scene.
    Timestamps: a scene has a start_time and an end_time
"""

# Define and call a scene using parse_scene function
scene = zl5.scenes[0]
scene
print('less ugly scenes dictionary \n', parse_scene(scene))

# =====================================================================
# CLASSES:
# CLS1:BaseParser
class BaseParser:
    """
    A robust and fast interface to load l5kit data into  Pandas dataframes.

    Parameters
    ----------
    chunk_size: int, default=1000
        How many items do you want in a single slice. The larger the better;
        as long as you have enough memory. Nevertheless, chunk sizes above `10_000` won't lead to
        significant speed gain as the original zarr files was chunked at 10_000.

    max_chunks: int, default=10
        How many chunks do you want to read from memory.

    root:
        Zarr data root path

    zarr_path:
        relative path or key to the data.
    """

    field = "scenes"
    dtypes = {}

    def __init__(self, start=0, end=None, chunk_size=1000, max_chunks=10, root=DATA_ROOT,
                 zarr_path="scenes"):

        self.start = start
        self.end = end
        self.chunk_size = chunk_size
        self.max_chunks = max_chunks

        self.root = Path(root)
        assert self.root.exists(), "There is nothing at {}!".format(self.root)
        self.zarr_path = Path(zarr_path)

    def parse(self):
        raise NotImplementedError

    def to_pandas(self, start: object = 0, end: object = None, chunk_size: object = None, max_chunks: object = None) -> object:
        start = start or self.start
        end = end or self.end
        chunk_size = chunk_size or self.chunk_size
        max_chunks = max_chunks or self.max_chunks

        if not chunk_size or not max_chunks:  # One shot load, suitable for small zarr files
            df = zarr.load(self.root.joinpath(self.zarr_path).as_posix())
            df = df[start:end]
            df = map(self.parse, df)
        else:  # Chunked load, suitable for large zarr files
            df = []
            with zarr.open(self.root.joinpath(self.zarr_path).as_posix(), "r") as zf:
                end = start + max_chunks * chunk_size if end is None else min(end, start + max_chunks * chunk_size)
                for i_start in range(start, end, chunk_size):
                    items = zf[self.field][i_start: min(i_start + chunk_size, end)]
                    items = map(self.parse, items)
                    df.append(items)
            df = it.chain(*df)

        df = pd.DataFrame.from_records(df)
        for col, col_dtype in self.dtypes.items():
            df[col] = df[col].astype(col_dtype, copy=False)
        return df


# CLS2:SceneParser
class SceneParser(BaseParser):
    field = "scenes"

    @staticmethod
    def parse(scene):
        scene_dict = {
            "frame_index_interval_start": scene[0][0],
            "frame_index_interval_end": scene[0][1],
            "host": scene[1],
            "start_time": scene[2],
            "end_time": scene[3]
        }
        return scene_dict

# =====================================================================

sp = SceneParser(chunk_size=None, max_chunks=None, zarr_path="scene")
scenes = sp.to_pandas()

print(scenes.shape) #nothing is printed - this should've given: (100,5)
print(scenes.head()) #nothing is printed - a schedule for scenes data

scenes.describe()


#Too many errors Stopping now and coming back later [Israa-9/3/21]
