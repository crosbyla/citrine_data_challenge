import os
import argparse
import pandas as pd
import pypif.pif as pif
from pypif.obj import ChemicalSystem, Property, Id, License, Person, Reference,\
        ProcessStep, Software, Scalar, Name


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
    pif_data.contacts = [
        Person(
            name=Name(given='Lawrence', family='Crosby'),
            email='crosbyla@u.northwestern.edu',
            orcid='0000-0001-7644-3762'
        )
    ]

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
    num_atoms = Property(name='Number of Atoms', dataType='COMPUTATIONAL')
    n_atoms = df.iloc[0, 0]
        # get n_atoms from first element of DataFrame
    num_atoms.scalars = [Scalar(value=n_atoms)]
    properties.append(num_atoms)

    atoms = Property(name='Atoms', dataType='COMPUTATIONAL')
    elems = [df.iloc[a, 0] for a in range(2, int(n_atoms)+2)]
        # set elements using 1st column starting from 2nd row of DateFrame
    atoms.scalars = [Scalar(elem) for elem in elems]
    properties.append(atoms)

    atomic_positions = Property(name='Atomic Positions',
                                dataType='COMPUTATIONAL', units='angstrom')
    x_coords = [df.iloc[a, 1] for a in range(2, int(n_atoms)+2)]
    y_coords = [df.iloc[a, 2] for a in range(2, int(n_atoms)+2)]
    z_coords = [df.iloc[a, 3] for a in range(2, int(n_atoms)+2)]
        # set coordinates using 2nd, 3rd, and 4th columns starting from 2nd row of DateFrame
    atomic_positions.vectors = [
        [
            Scalar(x_coords[i]),
            Scalar(y_coords[i]),
            Scalar(z_coords[i])
        ]
        for i in range(int(n_atoms))
    ]
    properties.append(atomic_positions)

    partial_charges = Property(name='Partial Charge',
                               dataType='COMPUTATIONAL', units='e')
    charges = [df.iloc[a, 4] for a in range(2, int(n_atoms)+2)]
        # set charges using 5th columns starting from 2nd row of DateFrame
    partial_charges.scalars = [Scalar(charge) for charge in charges]
    properties.append(partial_charges)

    rot_a = Property(
                name='Rotational Constant A',
                dataType='COMPUTATIONAL',
                units='GHz',
                scalars=Scalar(value=df.iloc[1, 2])
            )
    properties.append(rot_a)

    rot_b = Property(
                name='Rotational Constant B',
                dataType='COMPUTATIONAL',
                units='GHz',
                scalars=Scalar(value=df.iloc[1, 3])
            )
    properties.append(rot_b)

    rot_c = Property(
                name='Rotational Constant C',
                dataType='COMPUTATIONAL',
                units='GHz',
                scalars=Scalar(value=df.iloc[1, 4])
            )
    properties.append(rot_b)

    mu = Property(
                name='Dipole Moment',
                dataType='COMPUTATIONAL',
                units='D',
                scalars=Scalar(value=df.iloc[1, 5])
         )
    properties.append(mu)

    alpha = Property(
                name='Isotropic Polarizability',
                dataType='COMPUTATIONAL',
                units='angstrom^3',
                scalars=Scalar(value=df.iloc[1, 6])
            )
    properties.append(alpha)

    e_homo = Property(
                name='Energy of HOMO',
                dataType='COMPUTATIONAL',
                units='Hartree',
                scalars=Scalar(value=df.iloc[1, 7])
            )
    properties.append(e_homo)

    e_lumo = Property(
                name='Energy of LUMO',
                dataType='COMPUTATIONAL',
                units='Hartree',
                scalars=Scalar(value=df.iloc[1, 8])
            )
    properties.append(e_lumo)

    e_gap = Property(
                name='Energy Gap',
                dataType='COMPUTATIONAL',
                units='Hartree',
                scalars=Scalar(value=df.iloc[1, 9])
            )
    properties.append(e_gap)

    r2 = Property(
                name='Electronic Spatial Extent',
                dataType='COMPUTATIONAL',
                units='angstrom^2',
                scalars=Scalar(value=df.iloc[1, 10])
         )
    properties.append(r2)

    zpve = Property(
                name='Zero Point Vibrational Energy',
                dataType='COMPUTATIONAL',
                units='Hartree',
                scalars=Scalar(value=df.iloc[1, 11])
           )
    properties.append(zpve)

    u_0 = Property(
                name='Internal Energy at OK',
                dataType='COMPUTATIONAL',
                units='Hartree',
                scalars=Scalar(value=df.iloc[1, 12])
          )
    properties.append(u_0)

    u = Property(
                name='Internal Energy at 298K',
                dataType='COMPUTATIONAL',
                units='Hartree',
                scalars=Scalar(value=df.iloc[1, 13])
        )
    properties.append(u)

    h = Property(
                name='Enthalpy at 298K',
                dataType='COMPUTATIONAL',
                units='Hartree',
                scalars=Scalar(value=df.iloc[1, 14])
        )
    properties.append(h)

    g = Property(
                name='Free Energy at 298K',
                dataType='COMPUTATIONAL',
                units='Hartree',
                scalars=Scalar(value=df.iloc[1, 15])
        )
    properties.append(g)

    c_v = Property(
                name='Heat Capacity at 298K',
                dataType='COMPUTATIONAL',
                units='cal/mol/K',
                scalars=Scalar(value=df.iloc[1, 16])
          )
    properties.append(c_v)

    pif_data.properties = properties

    return pif_data


def save_pif(pif_data, out_file=None, data_dir=os.getcwd()):
    """
    Saves PIF data to disk as PIF JSON file format

    :param: pif_data -  PIF System object
    :param: out_file -  Output file name, will default to pif GDB9 id number
    :param: data_dir -  Path to write output file, will default to current directory
    """
    if not out_file:
        out_file = os.path.join(data_dir, '{}.json'.format(pif_data.ids[0].value))

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
