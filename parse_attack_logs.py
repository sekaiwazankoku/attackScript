import matplotlib.pyplot as plt
import numpy as np
from common import try_except_wrapper
from typing import Literal
import argparse
import os

def plot(x, y, fpath,
            xlabel="", ylabel="",
            yscale: Literal['linear', 'log', 'symlog', 'logit'] = 'linear',
            title=""):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    # ax.set_yscale(yscale)
    ax.set_title(title)
    fig.set_tight_layout(True)
    fig.savefig(fpath)
    plt.close(fig)


def parse_log(data, fpath):
    f = open(fpath)
    for line in f:
        tokens = line.split(", ")
        for i, token in enumerate(tokens):
            pair = token.split(" ")
            data[pair[0]].append(float(pair[1]))
    f.close()
    return data


def parse_genericcc_log(fpath, output_dir):
    data = {"timestamp": [], "min_rtt": [], "rtt": [], "queuing_delay": [], "delta": []}
    data = parse_log(data, fpath)

    os.makedirs(output_dir, exist_ok=True)
    plot(data["timestamp"], data["min_rtt"], os.path.join(output_dir, 'genericcc_min_rtt.pdf'),
            xlabel='Time (ms)', ylabel='RTT (ms)')
    plot(data["timestamp"], data["rtt"], os.path.join(output_dir, 'genericcc_rtt.pdf'),
            xlabel='Time (ms)', ylabel='RTT (ms)')
    plot(data["timestamp"], data["queuing_delay"], os.path.join(output_dir, 'genericcc_queuing_delay.pdf'),
            xlabel='Time (ms)', ylabel='Queuing Delay (ms)')
    plot(data["timestamp"], data["delta"], os.path.join(output_dir, 'genericcc_delta.pdf'),
            xlabel='Time (ms)', ylabel='delta')


def parse_mahimahi_log(fpath, output_dir):
    data = {"timestamp": [], "delay": []}
    data = parse_log(data, fpath)

    os.makedirs(output_dir, exist_ok=True)
    plot(data["timestamp"][:500], data["delay"][:500], os.path.join(output_dir, 'mahimahi_delay.pdf'),
            xlabel='Time (ms)', ylabel='Computed Delay (ms)')


# @try_except_wrapper
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--type', required=True,
        type=str, action='store',
        help='attack log type: genericcc, mahimahi')
    parser.add_argument(
        '-i', '--input', required=True,
        type=str, action='store',
        help='path to mahimahi trace')
    parser.add_argument(
        '-o', '--output', required=True,
        type=str, action='store',
        help='path output figure')
    args = parser.parse_args()

    if args.type == "genericcc":
        parse_genericcc_log(args.input, args.output)
    elif args.type == "mahimahi":
        parse_mahimahi_log(args.input, args.output)
    else:
        print("No matching parsing function")
        


if(__name__ == "__main__"):
    main()
