import lasio

from wellbelog.belolas.schemas import LasCurvesSpecs


def open_las_file(path: str) -> lasio.las.LASFile:
    """
    Opens a LAS file and returns a LASFile object.
    """
    try:
        las_file = lasio.read(path)
        return las_file
    except Exception as e:
        return e


def process_curves_items(las_file: lasio.las.LASFile) -> LasCurvesSpecs:
    """
    Processes the curves items in a LAS file and returns a LasCurvesSpecs object.
    """
    curves = las_file.curves
    specs = []
    for curve in curves:
        curve_dict = curve.__dict__
        data = curve_dict.pop('data')
        spec = LasCurvesSpecs(**curve_dict, shape=data.shape)
        specs.append(spec)
    return specs
