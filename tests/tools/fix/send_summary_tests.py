from __future__ import annotations

from datetime import date
from email.message import EmailMessage
from pathlib import Path
import sys
import textwrap

import pytest

from api.app_string_provider import AppStringProvider
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_email_renderer import CheckEmailRenderer
from tools.checks.check_report import CheckReport
from tools.checks.check_report_parser import CheckReportParser
from tools.checks.color_token import ColorToken
from tools.checks.color_tokens import ColorTokens
from tools.checks.count import Count
from tools.checks.exhibit_region_colors import ExhibitRegionColors
from tools.checks.paths import Paths
from tools.fix.send_summary import SendSummary as send_summary
import tools.fix.send_summary as send_summary_module


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
      monkeypatch.delenv( send_summary.PASSWORD_VARIABLE, raising=False )
   else:
      monkeypatch.setenv( send_summary.PASSWORD_VARIABLE, password )

   monkeypatch.setattr(
      sys,
      'argv',
      [
         'fix',
         '--output',
         str( output ),
         '--exit-code',
         str( exit_code ),
      ],
   )
   return send_summary.main()


CLEAR_REPORT = f"""Wild encounter schedule check for 2026-11-04. Booking dates compared from 2026-11-05 through 2027-12-09.

{ CheckReport.category_line( 'checks.scheduledInAppOnly', 0 ) }

{ CheckReport.category_line( 'checks.scheduledOnWebsiteOnly', 0 ) }

Seasonal off-display check for 2026-11-04. The seasonal curves are not ramping down, so off-display flags were not compared.
Zoo hours check for 2026-11-04.

{ CheckReport.category_line( 'checks.websiteOnly', 1 ) }
  2027-01-01 to 2027-03-12 (71 days): open 09:30, last admission 15:30, close 16:30
    Website: daily

{ CheckReport.category_line( 'checks.appOnly', 0 ) }

""" + CheckReportParser.format_counts( zoo_hours=1 ) + """

""" + CheckReportParser.format_error_count( 1 ) + """
"""


def Test_ParseReport_TestSample_ExpectSectionsAndCounts() -> None:
   report = CheckReportParser.parse_report( CLEAR_REPORT )

   assert report.error_count == 1
   assert report.counts[ 0 ] == Count( label='Animals', count=0 )
   assert report.counts[ 1 ] == Count( label='Encounters', count=0 )
   assert report.counts[ -1 ] == Count( label='Zoo hours', count=1 )
   assert report.sections[ 0 ].kind == 'Wild encounter schedule'
   assert report.sections[ 0 ].note.startswith( CheckReport.text( 'checks.bookingDatesCompared' ) )
   assert report.sections[ 1 ].note.startswith( 'The seasonal curves' )
   assert report.sections[ 2 ].categories[ 0 ].count == 1
   assert report.sections[ 2 ].categories[ 0 ].items[ 0 ].title.startswith( '2027-01-01' )
   assert report.sections[ 2 ].categories[ 0 ].items[ 0 ].details == [ 'Website: daily' ]


def Test_RenderHtml_TestAnimalCatalogAndOffDisplay_ExpectOneSection() -> None:
   body = textwrap.dedent(
      f"""\
      { CheckReport.heading( 'seasonalOffDisplay', date( 2026, 11, 4 ) ) }

      { CheckReport.category_line( 'checks.offForSeasonWebsiteOnly', 1 ) }
        { AppStringProvider.format( 'format.middleDotPair', first='Polar Bear', second='Africa Savanna' ) }

      { CheckReport.category_line( 'checks.offForSeasonAppOnly', 1 ) }
        Marabou Stork

      Animal list check for 2026-11-04.

      { CheckReport.category_line( 'checks.websiteOnly', 1 ) }
        { AppStringProvider.format( 'format.middleDotPair', first='Capybara', second='Americas Pavilion' ) }

      { CheckReport.category_line( 'checks.appOnly', 0 ) }

      { CheckReportParser.format_counts( animals=3 ) }

      { CheckReportParser.format_error_count( 2 ) }
      """
   )
   html = CheckEmailRenderer.render_html( body, 1 )

   assert html.count( '>Animals<' ) == 2
   assert 'Animal list' not in html
   assert 'Animals off display' not in html
   assert CheckReport.text( 'checks.websiteOnly' ) in html
   assert 'Capybara' in html
   assert 'Americas Pavilion' in html
   colors = ExhibitRegionColors.exhibit_colors( 'Americas Pavilion' )
   assert colors.background in html
   assert colors.foreground in html
   assert CheckReport.text( 'checks.offForSeasonWebsiteOnly' ) in html
   assert 'Polar Bear' in html
   assert '<img ' not in html
   assert html.index( '>Animals<' ) < html.index( '>Encounters<' )
   assert html.index( '>Encounters<' ) < html.index( 'Polar Bear' )
   assert html.index( '>Encounters<' ) < html.index( 'Marabou Stork' )
   assert html.index( '>Encounters<' ) < html.index( 'Capybara' )


def Test_EmbedLocalImages_TestAppPhoto_ExpectShortContentId() -> None:
   photo = AnimalDetailImage.source( 'Africa Savanna', 'Red Panda' )
   embedded = CheckEmailRenderer.embed_local_images(
      f'<img src="{ CheckEmailRenderer.image_src( photo ) }">'
   )
   image = embedded.images[ 0 ]

   assert image.content_id.endswith( '@zoo.guide>' )
   assert 'ip6.arpa' not in image.content_id
   assert image.src() in embedded.html


def Test_RenderHtml_TestCorrectedOffDisplay_ExpectPhotoExhibitAndCorrection() -> None:
   photo = AnimalDetailImage.source( 'Kids Zoo', "Harris's Hawk" )
   body = textwrap.dedent(
      f"""\
      { CheckReport.heading( 'seasonalOffDisplay', date( 2026, 11, 7 ) ) }

      { CheckReport.category_line( 'checks.offForSeasonWebsiteOnly', 1 ) }
        { AppStringProvider.format( 'format.middleDotPair', first="Harris's Hawk", second='Kids Zoo' ) }
          { CheckReport.text( 'checks.photo' ) }{ photo }
          { CheckReport.text( 'checks.setOffDisplayForSeasonFrom' ) }November 7, 2026{ CheckReport.text( 'checks.dateThrough' ) }March 31, 2027{ CheckReport.text( 'checks.period' ) }

      { CheckReport.category_line( 'checks.offForSeasonAppOnly', 0 ) }

      { CheckReportParser.format_counts( animals=1 ) }

      { CheckReportParser.format_error_count( 1 ) }
      """
   )
   html = CheckEmailRenderer.render_html( body, 1 )
   colors = ExhibitRegionColors.exhibit_colors( 'Kids Zoo' )

   assert f'<span style="color:{ colors.foreground };">Harris&#x27;s Hawk</span>' in html
   assert 'Kids Zoo' in html
   assert colors.background in html
   assert colors.foreground in html
   image = CheckEmailRenderer.image_src( photo )
   label = f'<span style="color:{ colors.foreground };">Harris&#x27;s Hawk</span>'
   correction = CheckReport.text( 'checks.setOffDisplayForSeasonFrom' )
   assert image in html
   assert html.index( '>Encounters<' ) < html.index( image )
   assert html.index( image ) < html.index( label ) < html.index( correction )
   assert '</tr>' in html[ html.index( image ):html.index( label ) ]
   assert f'border:3px solid { colors.foreground }' in html
   assert 'white-space:nowrap' in html
   assert (
      CheckReport.text( 'checks.setOffDisplayForSeasonFrom' )
      + 'November 7, 2026'
      + CheckReport.text( 'checks.dateThrough' )
      + 'March 31, 2027'
      + CheckReport.text( 'checks.period' )
   ) in html
   assert CheckReport.text( 'checks.photo' ) not in html


def Test_RenderHtml_TestCorrectedAppOffDisplay_ExpectPhotoExhibitAndCorrection() -> None:
   photo = AnimalDetailImage.source( 'Kids Zoo', 'Abyssinian Ground Hornbill' )
   body = textwrap.dedent(
      f"""\
      { CheckReport.heading( 'seasonalOffDisplay', date( 2027, 3, 15 ) ) }

      { CheckReport.category_line( 'checks.offForSeasonAppOnly', 1 ) }
        { AppStringProvider.format( 'format.middleDotPair', first='Abyssinian Ground Hornbill', second='Kids Zoo' ) }
          { CheckReport.text( 'checks.photo' ) }{ photo }
          { CheckReport.text( 'checks.setOnDisplayForSeason' ) }

      { CheckReportParser.format_counts( animals=1 ) }

      { CheckReportParser.format_error_count( 1 ) }
      """
   )
   html = CheckEmailRenderer.render_html( body, 1 )
   colors = ExhibitRegionColors.exhibit_colors( 'Kids Zoo' )
   image = CheckEmailRenderer.image_src( photo )
   label = f'<span style="color:{ colors.foreground };">Abyssinian Ground Hornbill</span>'

   assert image in html
   assert label in html
   assert html.index( image ) < html.index( label )
   assert CheckReport.text( 'checks.setOnDisplayForSeason' ) in html
   assert CheckReport.text( 'checks.photo' ) not in html
   assert f'border:3px solid { colors.foreground }' in html


def Test_RenderHtml_TestOneErrorFixed_ExpectFixedHeadline() -> None:
   fixed = CheckReportParser.format_fixed_count( 1 )
   body = textwrap.dedent(
      f"""\
      Zoo hours check for 2026-11-04.

      { CheckReport.category_line( 'checks.websiteOnly', 2 ) }

      { CheckReport.category_line( 'checks.appOnly', 0 ) }

      { fixed }

      { CheckReportParser.format_counts( zoo_hours=2 ) }

      { CheckReportParser.format_error_count( 2 ) }
      """
   )
   report = CheckReportParser.parse_report( body )
   html = CheckEmailRenderer.render_html( body, 1 )

   detected = CheckReportParser.format_detected( 3, 1 )

   assert report.fixed_count == 1
   assert report.error_count == 2
   assert detected in html
   assert fixed not in html
   assert CheckReport.text( 'checks.status.differ' ) in html
   danger = ColorTokens.color( ColorToken.DANGER )
   assert f'color:{ danger };">{ detected }' in html


def Test_RenderHtml_TestFixedAndCatalogueMiss_ExpectGreenFixAndDangerMiss() -> None:
   fixed_title = CheckReport.text( 'checks.offForSeasonAppOnly' )
   missed_title = CheckReport.text( 'checks.websiteCatalogueNotInApp' )
   photo = AnimalDetailImage.source( 'Africa Savanna', 'Tiger' )
   body = textwrap.dedent(
      f"""\
      Seasonal off-display check for 2026-11-04.

      { CheckReport.category_line( 'checks.offForSeasonAppOnly', 1 ) }
        { AppStringProvider.format( 'format.middleDotPair', first='Warthog', second='Africa Savanna' ) }

      Animal list check for 2026-11-04.

      { CheckReport.category_line( 'checks.websiteCatalogueNotInApp', 1 ) }
        { AppStringProvider.format( 'format.middleDotPair', first='Tiger', second='Africa Savanna' ) }
          { CheckReport.text( 'checks.photo' ) }{ photo }

      { CheckReport.category_line( 'checks.appOnly', 0 ) }

      { CheckReportParser.format_fixed_count( 1 ) }

      { CheckReportParser.format_counts( animals=1 ) }

      { CheckReportParser.format_error_count( 1 ) }
      """
   )
   html = CheckEmailRenderer.render_html( body, 1 )
   green = ColorTokens.color( ColorToken.BRAND_PRIMARY )
   danger = ColorTokens.color( ColorToken.DANGER )
   detected = CheckReportParser.format_detected( 2, 1 )

   assert f'color:{ danger };">{ detected }' in html
   assert html.index( '>Encounters<' ) < html.index( 'Warthog' )
   assert f'color:{ green };">{ fixed_title }' in html
   assert f'color:{ danger };">{ missed_title }' in html
   assert CheckReport.text( 'checks.appOnly' ) not in html
   colors = ExhibitRegionColors.exhibit_colors( 'Africa Savanna' )
   assert f'color:{ colors.foreground };">Tiger' in html
   image = CheckEmailRenderer.image_src( photo )
   assert image in html
   assert html.index( image ) < html.index( '>Tiger<' )


def Test_RenderHtml_TestIssues_ExpectStyledDetails() -> None:
   html = CheckEmailRenderer.render_html( CLEAR_REPORT, 1 )

   assert CheckReport.text( 'checks.status.allClear' ) not in html
   assert CheckReport.text( 'checks.appOnly' ) not in html
   assert CheckReportParser.format_detected( 1, 0 ) in html
   assert CheckReportParser.format_fixed_count( 0 ) not in html
   assert 'Wednesday, November 4, 2026' in html
   assert 'Zoo hours' in html
   assert '2027-01-01 to 2027-03-12' in html
   assert 'The seasonal curves are not ramping down' not in html
   assert CheckReport.text( 'checks.bookingDatesCompared' ) not in html
   assert ColorTokens.color( ColorToken.BRAND_PRIMARY ) in html
   assert ColorTokens.color( ColorToken.DANGER ) in html


def Test_RenderHtml_TestClear_ExpectAllClear() -> None:
   body = textwrap.dedent(
      f"""\
      Zoo hours check for 2026-11-04.

      { CheckReport.category_line( 'checks.websiteOnly', 0 ) }

      { CheckReport.category_line( 'checks.appOnly', 0 ) }

      { CheckReportParser.format_counts() }

      { CheckReportParser.format_error_count( 0 ) }
      """
   )
   html = CheckEmailRenderer.render_html( body, 0 )

   assert CheckReport.text( 'checks.status.noneDetected' ) in html
   assert CheckReportParser.format_fixed_count( 0 ) not in html
   assert CheckReport.text( 'checks.status.websiteMatches' ) in html
   assert 'height:64px' in html[ html.index( 'Animals' ) - 240:html.index( 'Animals' ) ]
   assert 'height:64px' in html[ html.index( 'Guardians Talks' ) - 240:html.index( 'Guardians Talks' ) ]
   assert '2027-01-01' not in html


def Test_RenderHtml_TestFailure_ExpectMessage() -> None:
   html = CheckEmailRenderer.render_html(
      'Zoo hours check for 2026-11-04.\n\n'
      + CheckReportParser.format_error_count( 0 )
      + '\n',
      2,
   )

   assert CheckReport.text( 'checks.status.couldNotFinish' ) in html
   assert 'Wednesday, November 4, 2026' in html


def Test_SubjectFor_TestZeroErrors_ExpectSummarySubject() -> None:
   subject = CheckReportParser.subject_for(
      'detail\n\n' + CheckReportParser.format_error_count( 0 ) + '\n',
      0,
   )

   assert subject == (
      AppStringProvider.format( 'checks.subject.summary' )
      + CheckReportParser.format_error_count( 0 )
   )


def Test_SubjectFor_TestOneError_ExpectSummarySubject() -> None:
   subject = CheckReportParser.subject_for(
      'detail\n\n' + CheckReportParser.format_error_count( 1 ) + '\n',
      1,
   )

   assert subject == (
      AppStringProvider.format( 'checks.subject.summary' )
      + CheckReportParser.format_error_count( 1 )
   )


def Test_SubjectFor_TestFailedCheck_ExpectCouldNotFinish() -> None:
   subject = CheckReportParser.subject_for( 'Could not fetch the page.', 2 )

   assert subject == AppStringProvider.format( 'checks.subject.couldNotFinish' )


def Test_SendSummary_TestMessage_ExpectLoginAndSend(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   FakeSmtp.instances = []
   monkeypatch.setattr( send_summary_module.smtplib, 'SMTP', FakeSmtp )

   send_summary.send_summary(
      'Zoo hours check for 2026-11-04.\n\n'
      + CheckReportParser.format_error_count( 2 )
      + '\n',
      1,
      'app-password',
   )

   server = FakeSmtp.instances[ 0 ]
   message = server.sent
   assert server.host == send_summary.SMTP_HOST
   assert server.port == send_summary.SMTP_PORT
   assert server.timeout == 30
   assert server.started_tls
   assert server.logged_in == ( send_summary.EMAIL_ADDRESS, 'app-password' )
   assert server.quit_called
   assert message is not None
   assert message[ 'Subject' ] == (
      AppStringProvider.format( 'checks.subject.summary' )
      + CheckReportParser.format_error_count( 2 )
   )
   assert message[ 'From' ] == send_summary.EMAIL_ADDRESS
   assert message[ 'To' ] == send_summary.EMAIL_ADDRESS
   html = message.get_body( preferencelist=( 'html', ) ).get_content()
   assert CheckReportParser.format_error_count( 2 ) in html
   assert CheckReportParser.format_fixed_count( 0 ) not in html
   assert ColorTokens.color( ColorToken.BRAND_PRIMARY ) in html
   assert 'Toronto Zoo Guide' in html


def Test_SendSummary_TestAppPhoto_ExpectRelatedImage(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   photo = AnimalDetailImage.source( 'Africa Savanna', 'Warthog' )
   FakeSmtp.instances = []
   monkeypatch.setattr( send_summary_module.smtplib, 'SMTP', FakeSmtp )

   send_summary.send_summary(
      CheckReport.heading( 'seasonalOffDisplay', date( 2026, 11, 7 ) ) + '\n\n'
      + CheckReport.category_line( 'checks.offForSeasonWebsiteOnly', 1 )
      + '\n  '
      + AppStringProvider.format( 'format.middleDotPair', first='Warthog', second='Africa Savanna' )
      + '\n    '
      + CheckReport.text( 'checks.photo' )
      + photo
      + '\n\n'
      + CheckReportParser.format_error_count( 1 )
      + '\n',
      1,
      'app-password',
   )

   message = FakeSmtp.instances[ 0 ].sent
   html = message.get_body( preferencelist=( 'html', ) ).get_content()
   images = [
      part
      for part in message.walk()
      if part.get_content_maintype() == 'image'
   ]

   assert photo != ''
   assert 'cid:' in html
   assert 'file:' not in html
   assert images[ 0 ].get_content() == ( Paths.ROOT / photo ).read_bytes()


def Test_Main_TestMissingPassword_ExpectExitCode2(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   output = _output_file( tmp_path, CheckReportParser.format_error_count( 0 ) + '\n' )

   result = _run_main( monkeypatch, output, 0, None )

   captured = capsys.readouterr()
   assert result == 2
   assert send_summary.PASSWORD_VARIABLE in captured.err


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
   output = _output_file(
      tmp_path,
      'Zoo hours check for 2026-11-04.\n\n'
      + CheckReportParser.format_error_count( 0 )
      + '\n',
   )
   monkeypatch.setattr( send_summary_module.smtplib, 'SMTP', FailingSmtp )

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
      send_summary,
      'run_check',
      lambda: (
         'Zoo hours check for 2026-11-04.\n\n'
         + CheckReportParser.format_error_count( 0 )
         + '\n',
         0,
      ),
   )
   monkeypatch.setattr(
      send_summary,
      'open_preview',
      lambda path: opened.append( path ),
   )
   monkeypatch.setattr(
      sys,
      'argv',
      [ 'fix', '--preview', '--html', str( html_path ) ],
   )

   result = send_summary.main()

   captured = capsys.readouterr()
   assert result == 0
   assert opened == [ html_path ]
   assert CheckReport.text( 'checks.status.noneDetected' ) in html_path.read_text()
   assert str( html_path ) in captured.out


def Test_Main_TestSentSummary_ExpectExitCode0(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   output = _output_file(
      tmp_path,
      'Zoo hours check for 2026-11-04.\n\ndetail\n\n'
      + CheckReportParser.format_error_count( 0 )
      + '\n',
   )
   FakeSmtp.instances = []
   monkeypatch.setattr( send_summary_module.smtplib, 'SMTP', FakeSmtp )

   result = _run_main( monkeypatch, output, 0, 'app-password' )

   assert result == 0
   assert FakeSmtp.instances[ 0 ].sent is not None


def Test_SummaryLine_TestNothingFixed_ExpectNoErrorsDetected() -> None:
   body = (
      CheckReportParser.format_fixed_count( 0 )
      + '\n\n'
      + CheckReportParser.format_error_count( 0 )
      + '\n'
   )

   assert send_summary.summary_line( body ) == CheckReport.text( 'checks.status.noneDetected' )


def Test_SummaryLine_TestNothingFixedWithErrors_ExpectErrorCount() -> None:
   body = (
      CheckReportParser.format_fixed_count( 0 )
      + '\n\n'
      + CheckReportParser.format_error_count( 2 )
      + '\n'
   )

   assert send_summary.summary_line( body ) == CheckReportParser.format_detected( 2, 0 )


def Test_Main_TestNoArgs_ExpectCheckEmailed(
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   summary = CheckReportParser.format_detected( 2, 1 )
   report = (
      'Zoo hours check for 2026-11-04.\n\n'
      + CheckReportParser.format_fixed_count( 1 )
      + '\n\n'
      + CheckReportParser.format_error_count( 1 )
      + '\n'
   )
   FakeSmtp.instances = []
   monkeypatch.setattr( send_summary_module.smtplib, 'SMTP', FakeSmtp )
   monkeypatch.setenv( send_summary.PASSWORD_VARIABLE, 'app-password' )
   monkeypatch.setattr( send_summary, 'run_check', lambda: ( report, 1 ) )
   monkeypatch.setattr( sys, 'argv', [ 'fix' ] )

   result = send_summary.main()

   captured = capsys.readouterr()
   assert result == 1
   assert captured.out == summary + '\n'
   assert 'Zoo hours' not in captured.out
   assert report not in captured.err
   assert FakeSmtp.instances[ 0 ].sent is not None


def Test_Main_TestNoArgsMissingPassword_ExpectExitCode2(
      capsys: pytest.CaptureFixture[ str ],
      monkeypatch: pytest.MonkeyPatch ) -> None:
   def run_check() -> tuple[ str, int ]:
      raise AssertionError( 'run_check' )

   monkeypatch.delenv( send_summary.PASSWORD_VARIABLE, raising=False )
   monkeypatch.setattr( sys, 'argv', [ 'fix' ] )
   monkeypatch.setattr( send_summary, 'run_check', run_check )

   result = send_summary.main()

   captured = capsys.readouterr()
   assert result == 2
   assert send_summary.PASSWORD_VARIABLE in captured.err
