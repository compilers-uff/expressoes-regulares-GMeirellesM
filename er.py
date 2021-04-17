from operacoes import *
import sys


if len(sys.argv) > 1:
    args = sys.argv[1:]
    resp = "Not OK"

    if args[0] == '-f':

        arq = args[1]
        pal = args[2]

        arq = open(arq, 'r')
        ers = arq.readlines()

        for er in ers:
            er = er.rstrip('\n')
            result = match(er, pal)

            if result:
                resp = "OK"
            else:
                resp = "Not OK"

            print("match(" + er + "," + pal + ") == " + resp + "\n")

        arq.close()

    else:
        er = args[0]
        pal = args[1]
        result = match(er, pal)

        if result:
            resp = "OK"

        print("match(" + er + "," + pal + ") == " + resp + "\n")
