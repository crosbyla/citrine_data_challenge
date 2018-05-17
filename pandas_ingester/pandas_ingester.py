import os
import argparse
import pandas as pd
import pypif.pif as pif
from pypif.obj import ChemicalSystem


def load_data(data_file):
    """
    Loads GDB-9 XYZ files into memory as a Pandas dataframe
    input: GDB-9 xyz file (see DOI:10.1038/sdata.2014.22 for format
                            description)
    output: Pandas DataFrame with the GDB molecule information
    """
    lines = []

    # we must use Python read utilities instead of Pandas read_csv
    # because of unequal length rows
    with open(data_file) as fp:
        for line in fp:
            lines.append(line.strip('\n').split())

    df = pd.DataFrame(lines)

    return df


def make_pif(df):
    """
    Extracts information from Pandas Dataframe with GDB-9 molecule data
    to create a PIF object containing metadata and structural information
    input: Pandas Dataframe object
    output: PIF object
    """
    pif_data = ChemicalSystem()

    return pif_data


def save_pif(pif_data, data_dir=None, out_file=None):
    """
    Saves PIF data to disk as PIF JSON file format
    inputs:
        pif_data: PIF System object
        out_file: Path the write output file, will default to current directory
    """
    if not out_file:
        out_file = os.path.join(os.getcwd(), '{}.xyz'.format(pif_data.ids))

    with open(out_file, 'w') as fp:
        fp.write(pif.dumps(pif_data, indent=4))


def main(data_file):
    """
    Loads data from GDB-9 XYZ files as Pandas DataFrame, converts to the PIF
    format and writes file to disk as JSON format
    input: data_file, path to GDB-9 XYZ file on disk
    """

    df = load_data(data_file)
    pif_data = make_pif(df)

    save_pif(pif_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", help="path to input file")
    args = parser.parse_args()
    try:
        if args.data_file[-4] != '.xyz':
            raise ValueError('Must be XYZ file!')
    except IndexError:
        print('File name is too short')

    main(args.data_file)
