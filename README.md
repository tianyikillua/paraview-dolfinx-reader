# dolfinx HDF5 reader for arbitrary-order Lagrange elements

This repository contains a ParaView Python plugin (`dolfinxReader.py`) that can be loaded by ParaView to read the HDF5 mesh file written by [dolfinx](https://github.com/FEniCS/dolfinx) dedicated for arbitrary-order Lagrange elements.

Some code from [paraview-meshio-reader](https://github.com/tianyikillua/paraview-meshio-reader) is reused.

## Installation

1. Make sure that you have `h5py` installed in ParaView. You may simply copy the compatible `pip`-installed `h5py` directory into the ParaView Python environment.
2. Download `dolfinxReader.py` and load the plugin under ParaView, via *Tools* / *Manage Plugins* / *Load New*. You can optionally check the option *Auto Load*.

## License

`dolfinxReader.py` is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
