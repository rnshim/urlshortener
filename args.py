import argparse
import time

def get_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
  "--db-name",
  type=str,
  required=True,
  help="enter db name",
  )
  
  parser.add_argument(
  "--host",
  type=str,
  default="0.0.0.0",
  required=False,
  help="enter host",
  )
  
  parser.add_argument(
  "--port",
  type=int,
  default=8000,
  required=False,
  help="enter port number",
  )

  parser.add_argument(
  "--disable-random-alias",
  action="store_true",
  help="disable random alias",
  )

  parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="increase verbosity level",
  )

  return parser.parse_args()