from typing import List


def gen_bin_array(max_length=2) -> List[List[int]]:
    if max_length < 2:
        print("Minimum length is 2")
        exit(1)
    if max_length > 5:
        print("Maximum length is 5")
        exit(1)
    string_format = "".join(["{:0", str(max_length), "b}"])
    out = []
    for x in range(1 << max_length):
        out.append([int(d) for d in string_format.format(x)])
    return out

if __name__ == '__main__':
    dataset = gen_bin_array(3)
    [print("{},".format(e)) for e in dataset]
