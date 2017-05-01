from data_parser import parse

if __name__ == '__main__':
    data, err = parse("../data/terrain05.data")
    if err is not None:
        print("Error opening file:", err)
        exit(1)
    print(data)
