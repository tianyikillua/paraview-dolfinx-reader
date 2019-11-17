import numpy as np
from paraview.util.vtkAlgorithm import (
    VTKPythonAlgorithmBase,
    smdomain,
    smhint,
    smproperty,
    smproxy,
)
from vtkmodules.numpy_interface import dataset_adapter as dsa
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid

__author__ = "Tianyi Li"
__email__ = "tianyikillua@gmail.com"
__copyright__ = "Copyright (c) 2019 {} <{}>".format(__author__, __email__)
__license__ = "License :: OSI Approved :: MIT License"
__version__ = "0.0.1"
__status__ = "Development Status :: 4 - Beta"


# https://github.com/Kitware/VTK/blob/master/Common/DataModel/vtkCellType.h
dolfinx_to_vtk_type = {
    "interval": 68,
    "triangle": 69,
    "quadrilateral": 70,
    "tetrahedron": 71,
    "hexahedron": 72,
}
dolfinx_supported_ext = ["h5"]


@smproxy.reader(
    label="dolfinx Reader",
    extensions=dolfinx_supported_ext,
    file_description="dolfinx-supported files",
)
class dolfinxReader(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(
            self, nInputPorts=0, nOutputPorts=1, outputType="vtkUnstructuredGrid"
        )
        self._filename = None

    @smproperty.stringvector(name="FileName")
    @smdomain.filelist()
    @smhint.filechooser(
        extensions=dolfinx_supported_ext, file_description="dolfinx-supported files"
    )
    def SetFileName(self, filename):
        if self._filename != filename:
            self._filename = filename
            self.Modified()

    def RequestData(self, request, inInfo, outInfo):
        output = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(outInfo))

        # Use h5py to read the mesh
        import h5py

        f = h5py.File(self._filename, "r")
        mesh = f[list(f.keys())[0]]
        points = mesh["coordinates"][()]
        celltype = mesh["topology"].attrs["celltype"].decode("utf-8")
        cells = mesh["topology"][()]

        # Points
        if points.shape[1] == 2:
            points = np.hstack([points, np.zeros((len(points), 1))])
        output.SetPoints(points)

        # Cells
        vtk_type = dolfinx_to_vtk_type[celltype]
        ncells, npoints_per_cell = cells.shape
        cell_types = np.full(ncells, vtk_type, dtype=np.ubyte)
        cell_offsets = (1 + npoints_per_cell) * np.arange(ncells, dtype=int)
        cell_conn = np.hstack([npoints_per_cell * np.ones((ncells, 1), dtype=int), cells]).flatten()
        output.SetCells(cell_types, cell_offsets, cell_conn)

        return 1
