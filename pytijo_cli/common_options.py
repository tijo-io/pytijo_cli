import click
import logging


def set_logging_option(ctx, param, value):
    if value:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("set debug option on")
    else:
        logging.basicConfig(level=logging.ERROR)


TIJO_API_URL_OPTIONS = [
    click.option(
        "--tijo-base-api",
        type=click.STRING,
        default="http://api.tijo.io/v1",
        envvar="TIJO_API",
        help="Tijo base REST API endpoint",
    ),
    click.option(
        "--tijo-insecure",
        is_flag=True,
        default=False,
        help="Allow insecure https connections. SSL certificates are not validated if this option is given.",
    ),
    click.option("--tijo-timeout", type=click.INT, default=60, help="HTTP(s) timeout"),
]

GLOBAL_OPTIONS = [
    click.option(
        "--debug",
        "-d",
        is_flag=True,
        default=False,
        help="Print debug information",
        callback=set_logging_option,
    ),
]


def add_global_options():
    def _add_options(func):
        for option in reversed(GLOBAL_OPTIONS):
            func = option(func)
        return func

    return _add_options


def global_options(func):
    for option in reversed(GLOBAL_OPTIONS):
        func = option(func)
    return func


def add_tijoapi_url_options():
    def _add_url_options(func):
        for option in reversed(TIJO_API_URL_OPTIONS):
            func = option(func)
        return func

    return _add_url_options


def tijoapi_url_options(func):
    for option in reversed(TIJO_API_URL_OPTIONS):
        func = option(func)
    return func
