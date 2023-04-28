import uvicorn
from argparse import ArgumentParser
from backend.settings import UVICORN_CONFIG, APP_NAME


parser = ArgumentParser(APP_NAME)
parser.add_argument('-D', '--dev', action='store_true')

args = parser.parse_args()

if args.dev:
    uvicorn.run(**UVICORN_CONFIG)
else:
    raise NotImplementedError(
        'Production config is not implemented yet. Use -D/--dev to up development server.'
    )
