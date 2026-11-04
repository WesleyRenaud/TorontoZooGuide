from __future__ import annotations

from email.message import EmailMessage
from pathlib import Path
import sys

import pytest

import tools.emailCheckSummary as email_check_summary


class FakeSmtp():
   instances: list[ FakeSmtp ] = []


   def __init__( self, host: str, port: int, timeout: int ) -> None:
      self.host = host
      self.port = port
      self.timeout = timeout
      self.started_tls = False
      self.logged_in: tuple[ str, str ] | None = None
      self.sent: EmailMessage | None = None
      self.quit_called = False
      FakeSmtp.instances.append( self )


   def ehlo( self ) -> None:
      return None


   def starttls( self ) -> None:
      self.started_tls = True


   def login( self, username: str, password: str ) -> None:
      self.logged_in = ( username, password )


   def send_message( self, message: EmailMessage ) -> None:
      self.sent = message


   def quit( self ) -> None:
      self.quit_called = True


class FailingSmtp( FakeSmtp ):
   def login( self, username: str, password: str ) -> None:
      raise OSError( 'login failed' )


def _output_file( path: Path, body: str ) -> Path:
   output = path / 'check-output.txt'
   output.write_text( body )
   return output


def _run_main(
      monkeypatch: pytest.MonkeyPatch,
      output: Path,
      exit_code: int,
      password: str | None ) -> int:
   if password is None:
      monkeypatch.delenv( email_check_summary.PASSWORD_VARIABLE, raising=False )
   else:
      monkeypatch.setenv( email_check_summary.PASSWORD_VARIABLE, password )

   monkeypatch.setattr(
      sys,
      'argv',
      [
         'emailCheckSummary',
         '--output',
         str( output ),
         '--exit-code',
         str( exit_code ),
      ],
   )
   return email_check_summary.main()


def Test_SubjectFor_TestZeroErrors_ExpectSummarySubject() -> None:
   subject = email_check_summary.subject_for( 'detail\n\n0 errors\n', 0 )

   assert subject == 'Toronto Zoo check: 0 errors'


def Test_SubjectFor_TestOneError_ExpectSummarySubject() -> None:
   subject = email_check_summary.subject_for( 'detail\n\n1 error\n', 1 )

   assert subject == 'Toronto Zoo check: 1 error'


def Test_SubjectFor_TestFailedCheck_ExpectCouldNotFinish() -> None:
   subject = email_check_summary.subject_for( 'Could not fetch the page.', 2 )

   assert subject == 'Toronto Zoo check could not finish'


def Test_SendSummary_TestMessage_ExpectLoginAndSend(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   FakeSmtp.instances = []
   monkeypatch.setattr( email_check_summary.smtplib, 'SMTP', FakeSmtp )

   email_check_summary.send_summary( '2 errors\n', 1, 'app-password' )

   server = FakeSmtp.instances[ 0 ]
   message = server.sent
   assert server.host == email_check_summary.SMTP_HOST
   assert server.port == email_check_summary.SMTP_PORT
   assert server.timeout == 30
   assert server.started_tls
   assert server.logged_in == ( email_check_summary.EMAIL_ADDRESS, 'app-password' )
   assert server.quit_called
   assert message is not None
   assert message[ 'Subject' ] == 'Toronto Zoo check: 2 errors'
   assert message[ 'From' ] == email_check_summary.EMAIL_ADDRESS
   assert message[ 'To' ] == email_check_summary.EMAIL_ADDRESS
   assert '2 errors' in message.get_content()


def Test_Main_TestMissingPassword_ExpectExitCode2(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   output = _output_file( tmp_path, '0 errors\n' )

   result = _run_main( monkeypatch, output, 0, None )

   captured = capsys.readouterr()
   assert result == 2
   assert email_check_summary.PASSWORD_VARIABLE in captured.err


def Test_Main_TestMissingOutput_ExpectExitCode2(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   result = _run_main( monkeypatch, tmp_path / 'missing.txt', 0, 'app-password' )

   captured = capsys.readouterr()
   assert result == 2
   assert 'Could not find' in captured.err


def Test_Main_TestSmtpFailure_ExpectExitCode2(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   output = _output_file( tmp_path, '0 errors\n' )
   monkeypatch.setattr( email_check_summary.smtplib, 'SMTP', FailingSmtp )

   result = _run_main( monkeypatch, output, 0, 'app-password' )

   captured = capsys.readouterr()
   assert result == 2
   assert 'login failed' in captured.err


def Test_Main_TestSentSummary_ExpectExitCode0(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   output = _output_file( tmp_path, 'detail\n\n0 errors\n' )
   FakeSmtp.instances = []
   monkeypatch.setattr( email_check_summary.smtplib, 'SMTP', FakeSmtp )

   result = _run_main( monkeypatch, output, 0, 'app-password' )

   assert result == 0
   assert FakeSmtp.instances[ 0 ].sent is not None
