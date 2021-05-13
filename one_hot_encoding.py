""" encoding input sequence by character """


def bulk_encoder(input_path: str) -> list:
    res = list()

    sequences = list()
    with open(input_path) as input_fh:
        for line in input_fh:
            if line[0] == ">":
                continue
            sequences.append(line.strip())

    table = dict()
    for sequence in sequences:
        for char in sequence:
            if char.lower() not in table:
                table[char.lower()] = len(table)
    print(f"using characters: {','.join(table.keys())}")

    for sequence in sequences:
        res.append(one_hot_encoder(sequence, table))

    return res


def one_hot_encoder(sequence: str, table=dict()) -> list:
    res = list()

    encoding_size = len(table)
    if not table:
        for char in sequence:
            if char.lower() not in table:
                table[char.lower()] = len(table)
        encoding_size = len(table)
        print(f"using characters: {','.join(table.keys())}")

    for nt in sequence:
        one_hot_char = [0] * encoding_size
        one_hot_idx = table.get(nt.lower(), -1)
        one_hot_char[one_hot_idx] = 1
        res.append(one_hot_char)

    return res


if __name__ == "__main__":
    import argparse

    PARSER = argparse.ArgumentParser(description="one hot encoder")

    PARSER.add_argument("input", help="if --file yes, it would be path or seq")
    PARSER.add_argument("--file", type=str, default="no")

    ARGS = PARSER.parse_args()

    if ARGS.file == "yes":
        res = bulk_encoder(ARGS.input)
    else:
        res = one_hot_encoder(ARGS.input)

    print(res)