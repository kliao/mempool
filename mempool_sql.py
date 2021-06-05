#!/usr/bin/env python3
import json
import sys
import time
from subprocess import PIPE, Popen

MYSQL = "/usr/bin/mysql"
MEMPOOLLOG = "mempool.log"
MYSQLMEMPOOLDB = "btc_mempool"

FEELIMIT = [0.0001, 1, 2, 3, 4, 5, 6, 7, 8, 10,
            12, 14, 17, 20, 25, 30, 40, 50, 60, 70, 80, 100,
            120, 140, 170, 200, 250, 300, 400, 500, 600, 700, 800, 1000,
            1200, 1400, 1700, 2000, 2500, 3000, 4000, 5000, 6000, 7000, 8000, 10000]
sizes = [0] * len(FEELIMIT)
count = [0] * len(FEELIMIT)
fees = [0] * len(FEELIMIT)
found = False

SATOSHI_PER_BTC = 100000000


def parse_tx_data(obj):
    global sizes, count, fees, found
    if "fee" in obj or "fees" in obj:
        if "vsize" in obj:
            size = obj["vsize"]
        else:
            size = obj["size"]

        if "fees" in obj:
            fee = int(obj["fees"]["base"] * SATOSHI_PER_BTC)
            afees = int(obj["fees"]["ancestor"] * SATOSHI_PER_BTC)
            dfees = int(obj["fees"]["descendant"] * SATOSHI_PER_BTC)
        else:
            fee = int(obj["fee"] * SATOSHI_PER_BTC)
            afees = int(obj["descendantfees"])
            dfees = int(obj["descendantfees"])

        if "ancestorsize" in obj:
            asize = obj["ancestorsize"]
        else:
            asize = size

        if "descendantsize" in obj:
            dsize = obj["descendantsize"]
        else:
            dsize = size

        afpb = afees / asize  # ancestor fee (includes current)
        fpb = fee / size  # current fee
        dfpb = dfees / dsize  # descendant fee (includes current)
        # total average fee for mining all ancestors and descendants.
        tfpb = (afees + dfees - fee) / (asize + dsize - size)
        feeperbyte = max(min(dfpb, tfpb), min(fpb, afpb))

        found = True
        for i, limit in enumerate(FEELIMIT):
            if (feeperbyte >= limit and
                    (i == len(FEELIMIT) - 1 or feeperbyte < FEELIMIT[i + 1])):
                sizes[i] += size
                count[i] += 1
                fees[i] += fee
                break
        return None
    return obj


def dump_data(timestamp, sizes, count, fees):
    sizesstr = ",".join(str(x) for x in sizes)
    countstr = ",".join(str(x) for x in count)
    feesstr = ",".join(str(x) for x in fees)
    with open(MEMPOOLLOG, "a") as logfile:
        logfile.write("[{:d},[{}],[{}],[{}]],\n"
                      .format(timestamp, countstr, sizesstr, feesstr))
    # proc = Popen([MYSQL, MYSQLMEMPOOLDB], stdin=PIPE, stdout=PIPE)
    # proc.communicate("INSERT INTO mempool VALUES({:d},{},{},{});\n"
    #                 .format(timestamp, countstr, sizesstr, feesstr)
    #                 .encode("ascii"))


def main():
    global sizes, count, fees, found
    timestamp = int(time.time())
    json.load(sys.stdin, object_hook=parse_tx_data)
    if found:
        dump_data(timestamp, sizes, count, fees)


main()
