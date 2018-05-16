import pandas as pd
import pif


def load_data(data_file):
    """
    Loads GDB-9 XYZ files into memory as a Pandas dataframe
    input: GDB-9 xyz file (see DOI:10.1038/sdata.2014.22 for format description)
    output: Pandas DataFrame with the GDB molecule information
    """
    with open(data_file) as fp:
        for line in fp:
            lines.append(line.strip('\n').split('\t'))

    df = pd.DataFrame(lines)

    return df


def main():
    pass


if __name__ == '__main__':
    main()
