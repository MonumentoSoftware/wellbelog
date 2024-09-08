import json
import pathlib

from dlisio import dlis

from webelog.belodlis.objects_parsers.frame_parser import FrameProcessor
from webelog.belodlis.objects_parsers.logical_file_parser import get_logical_file_summary
from webelog.utils.logging import setup_logger
from .schemas.dlis import FrameDataframe, LogicalFileModel, PhysicalFileModel


def open_dlis_file(file_path: str) -> dlis.PhysicalFile:
    """
    Opens the DLIS file at the specified file path and returns a dlis.PhysicalFile object.

    Parameters:
        file_path (str): The path to the DLIS file.

    Returns:
        dlis.PhysicalFile: The opened DLIS file.

        Exception: If there is an error while loading the DLIS file.
    """
    try:
        return dlis.load(file_path)

    except Exception as e:
        raise e


def unpack_physical_dlis(ph_file: dlis.PhysicalFile) -> list[dlis.LogicalFile]:
    """
    Unpacks the physical file and returns a list of logical files
    """
    *logical_files, = ph_file
    return logical_files


class DlisManager:
    """
    This class is responsible for processing the dlis.PhysicalFile object
    """

    def __init__(self) -> None:
        self. logger = setup_logger(__class__.__name__)
        # sets a file to the logger output

    def process_physical_file(self, path: str, folder_name: str = None) -> PhysicalFileModel:
        """
        Process the PhysicalFile object and returns a PhysicalFileModel with the main data
        """
        # Creates a file name from the path and a BeloDlisWrapper object
        file_name = pathlib.Path(path).name

        # XXX Create a PhysicalFileModel object
        physical = PhysicalFileModel(file_name=file_name, logical_files=[], folder_name=folder_name)

        # NOTE This is to be used on a batch processing
        try:
            # Open the DLIS file or raise an exception
            file = open_dlis_file(path)
            logical_files = unpack_physical_dlis(file)

            # Process each logical file
            for file in logical_files:

                frames: list[dlis.Frame] = file.find('FRAME')
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

                # XXX Process each frame
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
                    # Append the frame model to the logical file
                    logical_file.frames.append(frame_model)

                    # XXX This is the end of the frame processing

                # Append the logical file to the physical file
                physical.logical_files.append(logical_file)
                # XXX This is the end of the logical file processing

            # Set the physical file to the wrapper
            return physical

        except Exception as e:
            self.logger.error(f'Error while processing the physical file: {e}')
            physical.error = True
            physical.error_message = str(e)
            return physical
