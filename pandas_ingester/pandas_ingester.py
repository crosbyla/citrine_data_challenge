import os
import argparse
import pandas as pd
import pypif.pif as pif
from pypif.obj import ChemicalSystem, Property, Id, License, Person, Reference,\
                      ProcessStep, Software, Scalar


def load_data(data_file):
    """
    Loads GDB-9 XYZ files into memory as a Pandas dataframe

    :param: GDB-9 xyz file (see DOI:10.1038/sdata.2014.22 for format
                            description)
    :return: Pandas DataFrame with the GDB molecule information
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

    :param: df - Pandas Dataframe object
    :return: PIF object
    """
    pif_data = ChemicalSystem()
    pif_data.references = [Reference(doi='10.1038/sdata.2014.22')]
    pif_data.licenses = [
            License(
                name='CC0 1.0',
                description='Creative Commons Public Domain Dedication',
                url='https://creativecommons.org/publicdomain/zero/1.0/'
                )
            ]
    software_list = [
            Software(name='Corina', version='3.491 2013', producer='Altamira LLC'),
            Software(name='MOPAC', version='13.136L 2012', producer='CAChe Research LLC')
            ]
    pif_data.preparation = [ProcessStep(software=software_list)]

    pif_data.chemical_formula = df.iloc[-1, 0].split('/')[1] # extract chem formula from InChI
        # set from last row, first element in DataFrame
    pif_data.uid = df.iloc[-1, 1] # use B3LYP InChI as uid
        # set from last row, second element in DataFrame

    ids = []
    gdb9_id = Id(name='GDB9 Id', value=df.iloc[1, 1])
    ids.append(gdb9_id)
    inchi_id_corina = Id(name='InChI Corina', value=df.iloc[-1, 0])
    ids.append(inchi_id_corina) # add Corina InChI to id list
    smiles_id_gdb17 = Id(name='SMILES GDB-17', value=df.iloc[-2, 0])
    ids.append(smiles_id_gdb17)# add SMILES GDB-17 to id list
    smiles_id_b3lyp = Id(name='SMILES B3LYP', value=df.iloc[-2, 1])
    ids.append(smiles_id_b3lyp)# add SMILES B3YLP to id list
    pif_data.ids = ids

    properties = []
    vib_freqs = Property(name='Harmonic Vibrational Frequencies', units='cm-1',
                         dataType='COMPUTATIONAL')
    vib_freqs.scalars = [Scalar(value=x) for x in df.iloc[-3, :]]
        # set vibrational frequencies using 3rd from last row in DataFrame

    properties.append(vib_freqs)

    pif_data.properties = properties

    return pif_data


def save_pif(pif_data, out_file=None, data_dir=os.getcwd()):
    """
    Saves PIF data to disk as PIF JSON file format

    :param: pif_data -  PIF System object
    :param: out_file -  Path the write output file, will default to current directory
    """
    if not out_file:
        out_file = os.path.join(data_dir, '{}.json'.format(pif_data.ids[0]))

    with open(out_file, 'w') as fp:
        fp.write(pif.dumps(pif_data, indent=4))


def main(data_file):
    """
    Loads data from GDB-9 XYZ files as Pandas DataFrame, converts to the PIF
    format and writes file to disk as JSON format

    :param: data_file - path to GDB-9 XYZ file on disk
    """

    df = load_data(data_file)
    pif_data = make_pif(df)

    save_pif(pif_data, out_file=data_file)


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
