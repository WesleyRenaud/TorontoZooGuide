from __future__ import annotations

import argparse
from email.message import EmailMessage
import os
from pathlib import Path
import smtplib
import sys


SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'wesleyrenaud736@gmail.com'
PASSWORD_VARIABLE = 'CHECK_EMAIL_PASSWORD'


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description='Email the daily Toronto Zoo website check summary.'
   )
   parser.add_argument(
      '--output',
      type=Path,
      required=True,
      help='File containing the check output.',
   )
   parser.add_argument(
      '--exit-code',
      type=int,
      required=True,
      help='Exit code from the check.',
   )
   return parser.parse_args()


def summary_line( body: str ) -> str | None:
   for line in reversed( body.splitlines() ):
      stripped = line.strip()

      if stripped == '1 error':
         return stripped

      count = stripped.removesuffix( ' errors' )

      if count.isdigit() and f'{ count } errors' == stripped:
         return stripped

   return None


def subject_for( body: str, exit_code: int ) -> str:
   if exit_code == 0 or exit_code == 1:
      line = summary_line( body )

      if line is not None:
         return f'Toronto Zoo check: { line }'

      return 'Toronto Zoo check finished'

   return 'Toronto Zoo check could not finish'


def send_summary( body: str, exit_code: int, password: str ) -> None:
   message = EmailMessage()
   message[ 'Subject' ] = subject_for( body, exit_code )
   message[ 'From' ] = EMAIL_ADDRESS
   message[ 'To' ] = EMAIL_ADDRESS
   message.set_content( body )
   server = smtplib.SMTP( SMTP_HOST, SMTP_PORT, timeout=30 )

   try:
      server.ehlo()
      server.starttls()
      server.ehlo()
      server.login( EMAIL_ADDRESS, password )
      server.send_message( message )
   finally:
      server.quit()


def main() -> int:
   args = parse_args()
   password = os.environ.get( PASSWORD_VARIABLE, '' )

   if password == '':
      print(
         f'Set the { PASSWORD_VARIABLE } secret to a Gmail app password.',
         file=sys.stderr,
      )
      return 2

   if not args.output.exists():
      print( f'Could not find { args.output }.', file=sys.stderr )
      return 2

   body = args.output.read_text()

   if body.strip() == '':
      body = 'The check produced no output.'

   try:
      send_summary( body, args.exit_code, password )
   except OSError as error:
      print( error, file=sys.stderr )
      return 2

   return 0


if __name__ == '__main__':
   raise SystemExit( main() )
