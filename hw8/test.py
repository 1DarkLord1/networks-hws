from stop_and_wait import calc_checksum, check_checksum


def test_cheksum_not_corrupted_1():
    msg = 'aaaajfjfjfjfsffdgfrsdfb232453562'.encode()
    checksum = calc_checksum(msg, base=4)
    assert check_checksum(checksum.to_bytes(4, 'big') + msg, base=4)


def test_cheksum_not_corrupted_2():
    msg = 'aAaAabacabaaaaaaaaaaaa3142432'.encode()
    checksum = calc_checksum(msg, base=4)
    assert check_checksum(checksum.to_bytes(4, 'big') + msg, base=4)


def test_cheksum_corrupted_1():
    msg = 'aaaajfjfjfjfsffdgfrsdfb232453562'.encode()
    checksum = calc_checksum(msg, base=4)
    checksum += 10
    assert not check_checksum(checksum.to_bytes(4, 'big')+ msg, base=4)


def test_cheksum_corrupted_2():
    msg = 'aAaAabacabaaaaaaaaaaaa3142432'.encode()
    checksum = calc_checksum(msg, base=4)
    checksum += 20
    assert not check_checksum(checksum.to_bytes(4, 'big') + msg, base=4)


if __name__ == '__main__':
    test_cheksum_not_corrupted_1()
    test_cheksum_not_corrupted_2()
    test_cheksum_corrupted_1()
    test_cheksum_corrupted_2()

    print(f'All tests passed')
