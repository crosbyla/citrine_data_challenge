# GDB-9 XYZ ingester

## Description

This package uses the Pandas library to ingest GDB-9 XYZ structure files into the Physical Information Format (PIF).
Metadata for the files is position-based, using the specification listed in Tables 2 and 3 at [dx.doi.org/10.1038/sdata.2014.22](https://dx.doi.org/10.1038/sdata.2014.22).

## Example

The data used for tests is from the QM9 database from the article listed above.
An example input data file can be found [here](pandas_ingester/data/dsgdb9nsd_017001.xyz).
The corresponding output file can be found [here](pandas_ingester/data/test.json).

## References

-  "Quantum chemistry structures and properties of 134 kilo molecules" [https://doi.org/10.6084/m9.figshare.978904](https://doi.org/10.6084/m9.figshare.978904)
- PyPIF [repo](https://github.com/CitrineInformatics/pypif)
- PIF schema [documentation](http://citrineinformatics.github.io/pif-documentation/)

## Requirements

### Installation

- Python 3.4 or greater
- pypif
- pandas >= 0.20

### Testing

- pytest >= 3.4.0
