from __future__ import annotations

import argparse
from email.message import EmailMessage
import os
from pathlib import Path
import smtplib
import subprocess
import sys
import tempfile

from api.app_string_provider import AppStringProvider
from tools.checks.check_email_renderer import CheckEmailRenderer
from tools.checks.check_exit_code import CheckExitCode
from tools.checks.check_report_parser import CheckReportParser
from tools.checks.paths import Paths


class SendSummary():
   SMTP_HOST = 'smtp.gmail.com'
   SMTP_PORT = 587
   EMAIL_ADDRESS = 'wesleyrenaud736@gmail.com'
   PASSWORD_VARIABLE = 'CHECK_EMAIL_PASSWORD'


   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      parser = argparse.ArgumentParser(
         description=AppStringProvider.format( 'checks.email.description' ),
      )
      parser.add_argument(
         '--preview',
         action='store_true',
         help=AppStringProvider.format( 'checks.email.preview' ),
      )
      parser.add_argument(
         '--output',
         type=Path,
         help=AppStringProvider.format( 'checks.email.output' ),
      )
      parser.add_argument(
         '--exit-code',
         type=int,
         help=AppStringProvider.format( 'checks.email.exitCode' ),
      )
      parser.add_argument(
         '--html',
         type=Path,
         default=Path( tempfile.gettempdir() ) / 'toronto-zoo-check-email.html',
         help=AppStringProvider.format( 'checks.email.html' ),
      )
      return parser.parse_args()


   @classmethod
   def run_check( cls ) -> tuple[ str, int ]:
      result = subprocess.run(
         [ sys.executable, '-m', 'tools.checks.schedule_checker' ],
         cwd=Paths.ROOT,
         capture_output=True,
         text=True,
         check=False,
      )
      return f'{ result.stdout }{ result.stderr }', result.returncode


   @classmethod
   def open_preview( cls, path: Path ) -> None:
      subprocess.run( [ 'open', str( path ) ], check=False )


   @classmethod
   def write_preview( cls, body: str, exit_code: int, path: Path ) -> None:
      path.write_text( CheckEmailRenderer.render_html( body, exit_code ) )


   @classmethod
   def preview( cls, args: argparse.Namespace ) -> int:
      body, exit_code = cls.run_check()
      cls.write_preview( cls.message_body( body ), exit_code, args.html )
      cls.open_preview( args.html )
      print( args.html )
      return CheckExitCode.CLEAR


   @classmethod
   def message_body( cls, body: str ) -> str:
      if body.strip() == '':
         return AppStringProvider.format( 'checks.email.noOutput' )

      return body


   @classmethod
   def summary_line( cls, body: str ) -> str:
      fixed = CheckReportParser.fixed_count( next(
         line
         for line in body.splitlines()
         if CheckReportParser.fixed_count( line ) != None
      ) )

      errors = CheckReportParser.summary_line( body )

      if fixed == 0 and errors == 0:
         return AppStringProvider.format( 'checks.status.noneDetected' )

      return CheckReportParser.format_detected( errors + fixed, fixed )


   @classmethod
   def send_summary( cls, body: str, exit_code: int, password: str ) -> None:
      message = EmailMessage()
      message[ AppStringProvider.format( 'checks.email.header.subject' ) ] = CheckReportParser.subject_for( body, exit_code )
      message[ AppStringProvider.format( 'checks.email.header.from' ) ] = cls.EMAIL_ADDRESS
      message[ AppStringProvider.format( 'checks.email.header.to' ) ] = cls.EMAIL_ADDRESS
      message.set_content( body )
      embedded = CheckEmailRenderer.embed_local_images(
         CheckEmailRenderer.render_html( body, exit_code )
      )
      message.add_alternative(
         embedded.html,
         subtype=AppStringProvider.format( 'checks.email.subtype' ),
      )
      html_part = message.get_body( preferencelist=( 'html', ) )

      if html_part != None:
         for image in embedded.images:
            html_part.add_related(
               image.path.read_bytes(),
               maintype='image',
               subtype='png',
               cid=image.content_id,
               disposition='inline',
               filename=image.path.name,
            )
      server = smtplib.SMTP( cls.SMTP_HOST, cls.SMTP_PORT, timeout=30 )

      try:
         server.ehlo()
         server.starttls()
         server.ehlo()
         server.login( cls.EMAIL_ADDRESS, password )
         server.send_message( message )
      finally:
         server.quit()


   @classmethod
   def run_and_send( cls ) -> int:
      password = os.environ.get( cls.PASSWORD_VARIABLE, '' )

      if password == '':
         print(
            AppStringProvider.format( 'checks.email.password' ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      body, exit_code = cls.run_check()
      print( cls.summary_line( body ) )

      try:
         cls.send_summary( cls.message_body( body ), exit_code, password )
      except OSError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      return exit_code


   @classmethod
   def main( cls ) -> int:
      args = cls.parse_args()

      if args.preview:
         return cls.preview( args )

      if args.output is None and args.exit_code is None:
         return cls.run_and_send()

      return cls.send( args )


   @classmethod
   def send( cls, args: argparse.Namespace ) -> int:
      if args.output is None or args.exit_code is None:
         print(
            AppStringProvider.format( 'checks.email.outputAndExitCode' ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      password = os.environ.get( cls.PASSWORD_VARIABLE, '' )

      if password == '':
         print(
            AppStringProvider.format( 'checks.email.password' ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      if not args.output.exists():
         print(
            AppStringProvider.format( 'checks.email.couldNotFindOutput' ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      try:
         cls.send_summary( cls.message_body( args.output.read_text() ), args.exit_code, password )
      except OSError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH

      return CheckExitCode.CLEAR


if __name__ == '__main__':
   raise SystemExit( SendSummary.main() )
