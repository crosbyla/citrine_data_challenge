# GDB-9 XYZ ingester

## Description

This package uses the Pandas library to ingest GDB-9 XYZ structure files into the Physical Information Format (PIF).
Metadata for the files is position-based, using the specification listed in Tables 2 and 3 at [dx.doi.org/10.1038/sdata.2014.22](https://dx.doi.org/10.1038/sdata.2014.22).

## Use

Install using setup.py

```shell
$ python setup.py install
```

To use either import ```pandas_ingester``` module and use the available functions, or from the command line user the ```pandas-ingester``` utility:

```shell
$ pandas-ingester testfile.xyz
```

By default, the output file will be a JSON fill and will be written to the same directory.
The file name will be based upon the gdb ID number.
Optionally, one can specify the output file name with the ```-o``` flag:

```shell
$ pandas-ingester testfile.xyz -o outfile.json
```

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
