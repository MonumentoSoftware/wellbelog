# Well Belo Log

The aim of Well Belo Log is to ease the workflow of dealing with large ammounts of files. It's quite common the need to restart your kernel while trying to acess some data in a closed file. Or maybe the boiler code is just too much, to merge the logical files, extract the frames... Anyway, enjoy...

The main design pattern of the Well Belo Log project is to mimmic the file structre of the dlis file, and the dlisio library, but with the dataframe extracted from the curves, stored on a BeloFrame. So instead of "raw" curves, you go straight to the dataframe.

So during the creation of a Well Belo Log file, all the frames are processed and transformed in a pandas.DataFrame, stored in the BeloFrame object.



