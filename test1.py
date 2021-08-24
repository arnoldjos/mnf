import argparse

from icmplib import ping


parser = argparse.ArgumentParser(description="Input country")
parser.add_argument('-j', '--jitter', type=float, default='5',
                    help='Maximum Jitter Value')
parser.add_argument('-l', '--latency', type=float, default='5',
                    help='Maximum Latency value')
parser.add_argument("host", metavar="host", help="The host address that will be tested")
args = parser.parse_args()

host = vars(args)["host"]
jitter = vars(args)["jitter"]
latency = vars(args)["latency"]
check = ping(host)


def main():
    if check.jitter > jitter or check.avg_rtt > latency:
        if check.jitter > jitter and check.avg_rtt > latency:
            print(f"JITTER AND LATENCY CRITICAL latency = {check.avg_rtt},jitter = {check.jitter} | ", end='')
        elif check.jitter > jitter:
            print(f"JITTER CRITICAL latency = {check.avg_rtt},jitter={check.jitter} | ", end='')
        else:
            print(f"JITTER AND LATENCY CRITICAL latency = {check.avg_rtt},jitter = {check.jitter} | ", end='')
        print(f"maxlatency = {latency},maxjitter = {jitter}")
    else:
        print(f"HOST OK - latency = {check.avg_rtt},jitter = {check.jitter}")


if __name__ == '__main__':
    main()

