# import click
import fcntl
import sys
import os

import click

from lib import DataHandler


@click.command()
@click.option('--kline', '-k', required=True, type=str)
@click.option('--lowerLimit', '-l', 'lowerLimit', type=int, default=-1, required=True)
@click.option('--upperLimit', '-u', 'upperLimit', type=int, default=-1, required=True)
def main(kline, lowerLimit, upperLimit):
    click.echo(
        f"kline size: {kline}, lowerLimit: {lowerLimit}, upperLimit: {upperLimit}"
    )

    datahandler = DataHandler.BinanceWrapper()
    pid_file = f'datarunner_{kline}_{lowerLimit}_{upperLimit}.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        # another instance is running
        click.echo("already running")
        sys.exit(1)
    numCryptos = len(datahandler.getcryptoSymbols(tether="USDT"))
    if upperLimit == -1 or lowerLimit == -1:
        datahandler.getAllCryptoDataBinance(kline_size=kline, save=True)
    elif (lowerLimit >= 0 and lowerLimit < upperLimit):
        upperLimit = min(upperLimit, numCryptos)
        datahandler.updateLimitedCryptoData(
            kline_size=kline, upperLimit=upperLimit, lowerLimit=lowerLimit)
    else:
        click.echo("Invalid upper and lower limits")
    os.remove(pid_file)
    print(
        f"completed kline size: {kline}, lowerLimit: {lowerLimit}, upperLimit: {upperLimit}"
    )


if __name__ == "__main__":
    main()
