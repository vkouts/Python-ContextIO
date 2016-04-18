def headerprint(label):
    print "\n\033[94m{0}\033[0m".format(label)
    print "------------------------------------------------------------------\n"

def cprint(label, val):
    print "\033[92m{0}:\033[0m {1}".format(label, val)
