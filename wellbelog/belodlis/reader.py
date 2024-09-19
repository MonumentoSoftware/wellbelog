import json
import pathlib
from typing import Optional

from dlisio.dlis import Frame

from wellbelog.utils.logging import setup_logger
from ..schemas.dlis import FrameDataframe, LogicalFileModel, PhysicalFileModel
from .objects_parsers.logical_file_parser import get_logical_file_summary
from .objects_parsers.frame_parser import FrameProcessor
from .functions import open_dlis_file, unpack_physical_dlis


class DlisReader:
    """
    This class is responsible for processing the dlis.PhysicalFile object
    """

    def __init__(self) -> None:
        self. logger = setup_logger(__class__.__name__)

    def load_raw(self, path_to_file: str, unpack=False) -> PhysicalFileModel:
        """
        Load a DLIS file and return the raw data.

        Args:
            path_to_file (str): Path to the DLIS file.

        Returns:
            PhysicalFileModel: The raw data.
        """
        file = open_dlis_file(pathlib.Path(path_to_file).absolute())
        if unpack:
            return unpack_physical_dlis(file)
        return file

    def search_files(self, path: str) -> Optional[list[pathlib.Path]]:
        """
        Search for DLIS files in the given path and returns a list with the file paths.

        Parameters:
            path (str): The path to the folder where the DLIS files are located.
        """
        dlis_files = []
        try:
            for file in pathlib.Path(path).rglob('*.dlis'):
                dlis_files.append(file)
            return dlis_files
        except Exception as e:
            self.logger.error(f'Error while searching for DLIS files: {e}')
            return None

    def process_physical_file(self, path: str, folder_name: str = None) -> PhysicalFileModel:
        """
        Process the PhysicalFile object and returns a PhysicalFileModel with the main data.

        Parameters:
            path (str): The path to the DLIS file.
            folder_name (str): The name of the folder where the file is located.
        """
        # Creates a file name from the path and a BeloDlisWrapper object
        file_name = pathlib.Path(path).name
        self.logger.info(f'Processing the file: {file_name}')
        # XXX Create a PhysicalFileModel object
        physical = PhysicalFileModel(file_name=file_name, logical_files=[], folder_name=folder_name)

        # NOTE This is to be used on a batch processing
        try:
            # Open the DLIS file or raise an exception
            file = open_dlis_file(pathlib.Path(path).absolute())
            logical_files = unpack_physical_dlis(file)

            # Process each logical file
            for file in logical_files:

                frames: list[Frame] = file.find('FRAME')
                logical_file = LogicalFileModel(
                    file_name=file_name,
                    logical_id=file.fileheader.id,
                    summary=get_logical_file_summary(file),
                    frames=[]
                )

                # If there are no frames, set the error flag and the error message
                if not frames:
                    logical_file.error = True
                    logical_file.error_message = 'No frames found in the logical file'
                    physical.error_files.append(logical_file)
                    continue

                # NOTE Process each frame
                # iterate over the frames and process each one
                for frame in frames:

                    # Create a frame model and process the frame,
                    # NOTE it will return None if the frame has a DUMM channel
                    frame_model = FrameProcessor.process_frame(frame, file_name=file_name, logical_id=file.fileheader.id)

                    # If 'DUMM' channel is found, set the error flag and the error message
                    if frame_model is None:
                        logical_file.error = True
                        logical_file.error_message = 'DUMM channel found in the frame'
                        physical.error_files.append(logical_file)
                        continue

                    # Process the frame and check for DUMM channels
                    data = FrameProcessor.dlis_curves_to_dataframe(frame)
                    # Check if the data is an exception
                    # If it is, set the error flag and the error message
                    if data is Exception:
                        frame_model.error = True
                        frame_model.error_message = data.__str__()
                        logical_file.error = True
                        logical_file.error_message = data.__str__()
                        logical_file.frames.append(frame_model)
                        physical.error_files.append(logical_file)
                        continue

                    # Create a frame data model
                    frame_data = FrameDataframe(
                        file_name=file_name,
                        logical_file_id=file.fileheader.id,
                        data=json.loads(data.to_json(orient='records')),
                    )
                    # Set the frame data to the frame model
                    frame_model.data = frame_data
                    logical_file.frames.append(frame_model)

                # Append the logical file to the physical file
                physical.logical_files.append(logical_file)

            return physical

        except Exception as e:
            self.logger.error(f'Error while processing the physical file: {e}')
            physical.error = True
            physical.error_message = str(e)
            return physical
