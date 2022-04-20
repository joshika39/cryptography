def letter_row(search_target: str, matrix: list) -> int:
    for row_index, row in enumerate(matrix):
        for row_letter in row:
            if row_letter == search_target:
                return row_index

    return -1


def letter_col(search_target: str, matrix: list) -> int:
    for row in matrix:
        for col_index, col_letter in enumerate(row):
            if col_letter == search_target:
                return col_index

    return -1


def shift_letter_hor(shift_letter: str, matrix: list, direction: int) -> str:
    row = letter_row(shift_letter, matrix)
    col = letter_col(shift_letter, matrix)
    length = len(matrix[row]) - 1
    if direction > 0:
        if col + 1 > length:
            return matrix[row][0]
        else:
            return matrix[row][col + 1]
    else:
        if col - 1 < 0:
            return matrix[row][length]
        else:
            return matrix[row][col - 1]


def shift_letter_ver(shift_letter: str, matrix: list, direction: int) -> str:
    row = letter_row(shift_letter, matrix)
    col = letter_col(shift_letter, matrix)
    length = len(matrix) - 1
    if direction > 0:
        if row + 1 > length:
            return matrix[0][col]
        else:
            if len(matrix[row + 1]) < len(matrix[row]):
                return matrix[0][col]
            else:
                return matrix[row + 1][col]
    else:
        if row - 1 < 0:
            return matrix[length][col]
        else:
            return matrix[row - 1][col]


def get_letter_from_number(num_code: int, matrix: list) -> str:
    row = num_code // 10
    col = num_code % 10
    return matrix[row - 1][col - 1]


def create_plain_text(charset: list, input_message: str) -> list:
    plaintext = []
    input_message = input_message.lower()
    input_iter = enumerate(input_message)
    for input_index, input_letter in input_iter:
        if input_index + 1 < len(input_message):
            cLetter = input_letter + input_message[input_index + 1]
            if charset.__contains__(cLetter + "s"):
                plaintext.append(cLetter + "s")
                next(input_iter)
                next(input_iter)
            elif charset.__contains__(cLetter):
                plaintext.append(cLetter)
                next(input_iter)
            else:
                plaintext.append(input_letter)
        else:
            plaintext.append(input_letter)
    return plaintext


def polybius_square_to_list(input_list: str) -> list:
    input_list_iter = enumerate(input_list)
    formatted = []
    pair = []
    for index, input_list_letter in input_list_iter:
        if input_list_letter == ' ':
            formatted.append([input_list_letter])
        elif index + 1 < len(input_list):
            num = int(input_list_letter + input_list[index + 1])
            next(input_list_iter)
            pair.append(num)
            if len(pair) >= 2:
                formatted.append(pair)
                pair = []
    return formatted


def string_to_list(input_list) -> list:
    input_list_iter = enumerate(input_list)
    formatted = []
    for index, input_list_letter in input_list_iter:
        if input_list_letter == ' ':
            formatted.append([input_list_letter])
        elif index + 1 < len(input_list):
            if input_list[index + 1] == ' ':
                formatted.append([input_list_letter, fillerLetter])
                continue
            if input_list_letter == input_list[index + 1]:
                formatted.append([input_list_letter, fillerLetter])
                continue
            else:
                formatted.append([input_list_letter, input_list[index + 1]])
                next(input_list_iter)
        else:
            formatted.append([input_list_letter, fillerLetter])
    return formatted


def list_to_string(source_list: list) -> str:
    ret_string = ""
    for pair in source_list:
        for pair_index, pair_char in enumerate(pair):
            ret_string += str(pair_char)
    return ret_string


def encode(source_list: list, charset: list, direction: int) -> list:
    target_list = []
    for pair in source_list:
        if pair[0] == ' ':
            target_list.append([' '])
        elif letter_row(pair[0], charset) == letter_row(pair[1], charset):
            target_list.append(
                [shift_letter_hor(pair[0], charset, direction), shift_letter_hor(pair[1], charset, direction)])
        elif letter_col(pair[0], charset) == letter_col(pair[1], charset):
            target_list.append(
                [shift_letter_ver(pair[0], charset, direction), shift_letter_ver(pair[1], charset, direction)])
        else:
            target_list.append([
                charset[letter_row(pair[0], charset)][letter_col(pair[1], charset)],
                charset[letter_row(pair[1], charset)][letter_col(pair[0], charset)]])
    return target_list


def encode_polybios(source_list: list, charset: list, direction: int) -> list:
    target_list = []
    for pair in source_list:
        if direction > 0:
            if pair[0] == ' ':
                target_list.append([' '])
            else:
                target_list.append([(letter_row(pair[0], charset) + 1) * 10 + (letter_col(pair[0], charset) + 1),
                                    (letter_row(pair[1], charset) + 1) * 10 + (letter_col(pair[1], charset) + 1)])
        else:
            if pair[0] == ' ':
                target_list.append([' '])
            else:
                target_list.append([get_letter_from_number(int(pair[0]), charset),
                                    get_letter_from_number(int(pair[1]), charset)])
    return target_list


def key_string_to_list(key_string: str) -> list:
    kList = []
    key_enum = enumerate(key_string)
    for key_index, key_letter in key_enum:
        if key_index + 1 < len(key_string):
            if key_string[key_index + 1] == "/":
                kList.append(key_letter + key_string[key_index + 1] + key_string[key_index + 2])
                next(key_enum)
                next(key_enum)
            elif not kList.__contains__(key_letter):
                kList.append(key_letter)
        elif not kList.__contains__(key_letter):
            kList.append(key_letter)
    return kList


def create_alphabet_charset(alphabet_file: str, key_string: str) -> list:
    with open(alphabet_file, encoding='utf8') as f:
        lines = f.readlines()
    lines[0] = lines[0].strip()
    alphabet = lines[0].split(" ")

    tmp = []
    for key in key_string_to_list(key_string):
        tmp.append(key)

    for letter in alphabet:
        if not tmp.__contains__(letter):
            tmp.append(letter)

    table_size = 0
    for i in range(10):
        if pow(i, 2) <= len(alphabet):
            table_size = i

    table = []
    while tmp:
        table.append(tmp[:table_size])
        tmp = tmp[table_size:]

    return table


fillerLetter = 'x'
# text = input("Enter a message: ")
polybius_str = input("Enter the polybius numbers: ")
key_str = input("Enter the key: ")

cipher = create_alphabet_charset("EN-alphabet.txt", key_str)

# for line in cipher:
#     for char in line:
#         print(char + "\t", end='')
#     print("\n")


# pairs = string_to_list(create_plain_text(cipher, text))
# print(pairs)
#
# encoded_pairs = encode(pairs, cipher, 1)
# print(encoded_pairs)
#
# encoded_pairs_polybios = encode_polybios(encoded_pairs, cipher, 1)
# print(encoded_pairs_polybios)
#
# encoded_text_polybios = list_to_string(encoded_pairs_polybios)
# print(encoded_text_polybios)
#
# re_encoded_pairs_polybios = polybius_square_to_list(encoded_text_polybios)
# print(re_encoded_pairs_polybios)

polybius_pairs = polybius_square_to_list(polybius_str)
decoded_polybius_pairs = encode_polybios(polybius_pairs, cipher, -1)
decoded_pairs = encode(decoded_polybius_pairs, cipher, -1)
print(list_to_string(decoded_pairs))

