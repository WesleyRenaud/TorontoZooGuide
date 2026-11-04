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


CLEAR_REPORT = """Wild encounter schedule check for 2026-11-04. Booking dates compared from 2026-11-05 through 2027-12-09.

Scheduled in the app and not on the website: 0

Scheduled on the website and not in the app: 0

Seasonal off-display check for 2026-11-04. The seasonal curves are not ramping down, so off-display flags were not compared.
Zoo hours check for 2026-11-04.

On the website and not in the app: 1
  2027-01-01 to 2027-03-12 (71 days): open 09:30, last admission 15:30, close 16:30
    Website: daily

In the app and not on the website: 0

0 for encounters, 0 for Guardians Talks, 0 for animals, 0 for attractions, 0 for restaurants, 0 for gift shops, 0 for drinking fountains, 0 for the animal list, 0 for the attraction list, 0 for the restaurant list, 0 for the gift shop list, 1 for zoo hours

1 error
"""


def Test_ParseReport_TestSample_ExpectSectionsAndCounts() -> None:
   report = email_check_summary.parse_report( CLEAR_REPORT )

   assert report.errors == '1 error'
   assert report.counts[ 0 ] == ( 'Encounters', 0 )
   assert report.counts[ -1 ] == ( 'Zoo hours', 1 )
   assert report.sections[ 0 ].kind == 'Wild encounter schedule'
   assert report.sections[ 0 ].note.startswith( 'Booking dates compared' )
   assert report.sections[ 1 ].note.startswith( 'The seasonal curves' )
   assert report.sections[ 2 ].categories[ 0 ].count == 1
   assert report.sections[ 2 ].categories[ 0 ].items[ 0 ].title.startswith( '2027-01-01' )
   assert report.sections[ 2 ].categories[ 0 ].items[ 0 ].details == [ 'Website: daily' ]


def Test_RenderHtml_TestIssues_ExpectStyledDetails() -> None:
   html = email_check_summary.render_html( CLEAR_REPORT, 1 )

   assert 'All clear' not in html
   assert '1 error' in html
   assert 'Wednesday, November 4, 2026' in html
   assert 'Zoo hours' in html
   assert '2027-01-01 to 2027-03-12' in html
   assert 'The seasonal curves are not ramping down' not in html
   assert 'Booking dates compared' not in html
   assert email_check_summary.GREEN in html
   assert email_check_summary.DANGER in html


def Test_RenderHtml_TestClear_ExpectAllClear() -> None:
   body = """Zoo hours check for 2026-11-04.

On the website and not in the app: 0

In the app and not on the website: 0

0 for encounters, 0 for Guardians Talks, 0 for animals, 0 for attractions, 0 for restaurants, 0 for gift shops, 0 for drinking fountains, 0 for the animal list, 0 for the attraction list, 0 for the restaurant list, 0 for the gift shop list, 0 for zoo hours

0 errors
"""
   html = email_check_summary.render_html( body, 0 )

   assert 'All clear' in html
   assert 'The website and the app match.' in html
   assert '2027-01-01' not in html


def Test_RenderHtml_TestFailure_ExpectMessage() -> None:
   html = email_check_summary.render_html( 'Could not fetch the page.', 2 )

   assert 'Could not finish' in html
   assert 'Could not fetch the page.' in html


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
   html = message.get_body( preferencelist=( 'html', ) ).get_content()
   assert '2 errors' in html
   assert '#5e9600' in html
   assert 'Toronto Zoo Guide' in html


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


def Test_Main_TestPreview_ExpectOpenedHtml(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   html_path = tmp_path / 'email.html'
   opened: list[ Path ] = []
   monkeypatch.setattr(
      email_check_summary,
      'run_check',
      lambda: ( 'Zoo hours check for 2026-11-04.\n\n0 errors\n', 0 ),
   )
   monkeypatch.setattr(
      email_check_summary,
      'open_preview',
      lambda path: opened.append( path ),
   )
   monkeypatch.setattr(
      sys,
      'argv',
      [ 'emailCheckSummary', '--preview', '--html', str( html_path ) ],
   )

   result = email_check_summary.main()

   captured = capsys.readouterr()
   assert result == 0
   assert opened == [ html_path ]
   assert 'All clear' in html_path.read_text()
   assert str( html_path ) in captured.out


def Test_Main_TestPreviewFile_ExpectSkippedCheck(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   output = _output_file( tmp_path, 'Could not fetch the page.' )
   html_path = tmp_path / 'email.html'
   opened: list[ Path ] = []

   def fail_if_called() -> tuple[ str, int ]:
      raise AssertionError( 'preview used the saved output' )

   monkeypatch.setattr( email_check_summary, 'run_check', fail_if_called )
   monkeypatch.setattr(
      email_check_summary,
      'open_preview',
      lambda path: opened.append( path ),
   )
   monkeypatch.setattr(
      sys,
      'argv',
      [
         'emailCheckSummary',
         '--preview',
         '--output',
         str( output ),
         '--exit-code',
         '2',
         '--html',
         str( html_path ),
      ],
   )

   result = email_check_summary.main()

   assert result == 0
   assert opened == [ html_path ]
   assert 'Could not fetch the page.' in html_path.read_text()


def Test_Main_TestSentSummary_ExpectExitCode0(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   output = _output_file( tmp_path, 'detail\n\n0 errors\n' )
   FakeSmtp.instances = []
   monkeypatch.setattr( email_check_summary.smtplib, 'SMTP', FakeSmtp )

   result = _run_main( monkeypatch, output, 0, 'app-password' )

   assert result == 0
   assert FakeSmtp.instances[ 0 ].sent is not None
