
from typing import Any, Union

from pydantic import BaseModel, Field
from dlisio import dlis
import pandas as pd
import numpy as np

from webelog.belodlis.schemas.dlis import ChannelsList, FrameChannel, FrameModel
from webelog.utils.mnemonicfix import MnemonicFix


class FrameProcessor:
    """
    This class is responsible for processing the dlis.Frame object
    """
    @staticmethod
    def process_frame(frame: dlis.Frame, file_name: str, logical_id: str, filter: bool = True) -> Union[FrameModel, None]:
        """
        Process the Frame object and returns a dict with the main data
        """
        if filter:
            if 'DUMM' in [c.name for c in frame.channels]:
                return None

        model = FrameModel(
            file_name=file_name,
            logical_file_id=logical_id,
            description=str(frame.description) if frame.description else None,
            channels=FrameProcessor.processs_frame_channels(frame),
        )

        return model

    @ staticmethod
    def processs_frame_channels(frame: dlis.Frame, filter_dumm: bool = True) -> Union[ChannelsList, None]:
        """
        Tries to create a list of FrameChannelData from the Frame.channels
        """

        channels: list[dlis.Channel] = frame.channels
        if filter_dumm:
            if any([c.name == 'DUMM' for c in channels]):
                return None

        if not channels:
            return None

        channel_main_dict = [
            FrameChannel(
                long_name=str(channel.long_name),
                name=MnemonicFix.replace_index(str(channel.name)).strip(),
                units=str(channel.units),
                repr=str(channel.reprc),
                properties=str(channel.properties),

            )
            for channel in channels
        ]
        return channel_main_dict

    @ staticmethod
    def dlis_curves_to_dataframe(frame: dlis.Frame):
        """Tries to create a dataframe from the Frame.curves"""
        # Creating the main dataframe for the curve data
        try:
            df = pd.DataFrame(frame.curves())
            # - Fixing mnemonics and wrong indexes
            df = MnemonicFix.index_to_depth(df)
            df.columns = df.columns.str.strip()
            # Setting the column Well to the origin
            return df

        except ValueError as v:
            raise v

        except Exception as e:
            # NOTE It returns the Exception object
            # NOTE It will be setted to the Error in the BeloFrame
            return e
