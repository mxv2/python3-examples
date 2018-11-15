def prompt_int(msg, minimum, default, maximum=None):
    while True:
        try:
            line = input(msg)
            if not line and default is not None:
                return default
            i = int(line)
            if i < minimum:
                print("must be >=", minimum)
                continue
            if maximum is not None and i > maximum:
                print("must be <=", maximum)
                continue
            return i
        except ValueError as err:
            print(err)

