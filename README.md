# GDB-9 XYZ ingester

This package uses the Pandas library to ingest GDB-9 XYZ structure files into the Physical Information Format (PIF).
The file format should follow the specification listed at [dx.doi.org/10.1038/sdata.2014.22](dx.doi.org/10.1038/sdata.2014.22).

The data used for tests is from the QM9 database from the article "Quantum chemistry structures and properties of 134 kilo molecules", which can be found here: [https://doi.org/10.6084/m9.figshare.978904](https://doi.org/10.6084/m9.figshare.978904).

## Requirements

- pytest
- pypif
- pandas >= 0.20
