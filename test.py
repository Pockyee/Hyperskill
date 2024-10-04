def calculate_checksum(card_number):
    digits = [int(d) for d in str(card_number)]
    checksum = 0
    reverse_digits = digits[::-1]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 0:
            doubled = digit * 2
            if doubled > 9:
                doubled -= 9
            checksum += doubled
        else:
            checksum += digit
    return (10 - (checksum % 10)) % 10

card_number = "4000000777302995"  # 示例信用卡号
print (calculate_checksum(card_number))

print (calculate_checksum(card_number [:15]))
print (card_number[15])

print(card_number[15] != calculate_checksum(card_number [:15]))

print(1!=1)