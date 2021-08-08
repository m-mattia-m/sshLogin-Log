def formatNumber(self, number):
    number = str(number).replace("['  ", "")
    number = str(number).replace(r"\n']", "")
    i = 0
    print("Len: " + str(len(number)))

    length = int(len(number))
    while i < length:
        print("i: " + str(i))
        if i % 3 == 0:
            print("i-dritte-Stelle: " + str(i))
            tempNumber = ""
            packet1 = number[length - 3: length]
            packet2 = number[length - 6: length - 3]
            tempNumber = packet2 + "'" + packet1
            number = tempNumber
            pass
        i += 1
        pass

    return number
    pass