from __future__ import annotations

from datetime import date
from pathlib import Path
import sqlite3

import pytest

from api.animals.domain.animal_species_exhibit import AnimalSpeciesExhibit
from api.animals.domain.temporary_off_display_animal import TemporaryOffDisplayAnimal
from api.animals.status.animal_viewing_alert import AnimalViewingAlert
from api.models import Update
from api.updates.domain.update_type import UpdateType
from tools.checks.animal_detail_image import AnimalDetailImage
from tools.checks.check_report import CheckReport
from tools.checks.closure_viewing_alert import ClosureViewingAlert
from tools.checks.closure_viewing_alert_checker import ClosureViewingAlertChecker
from tools.checks.paths import Paths
from tools.checks.viewing_alert_sentence import ViewingAlertSentence


TODAY = date( 2026, 11, 13 )
SENTENCE = 'The polar bears can be seen in the pool at Tundra Trek. Underwater viewing is closed.'
SCHEMA = """
CREATE TABLE ZooUpdate (
   TITLE TEXT NOT NULL,
   DESCRIPTION TEXT NOT NULL,
   UPDATE_TYPE TEXT NOT NULL,
   START_DATE TEXT NOT NULL,
   END_DATE TEXT,
   PRIMARY KEY (TITLE, START_DATE)
);

CREATE TABLE Enclosure (
   SPECIES TEXT,
   EXHIBIT TEXT
);

CREATE TABLE AnimalStatus (
   SPECIES TEXT,
   EXHIBIT TEXT,
   IS_OFF_DISPLAY INTEGER,
   OFF_DISPLAY_FOR_SEASON INTEGER,
   VIEWING_SCOPE TEXT,
   OFF_DISPLAY_START TEXT,
   OFF_DISPLAY_END TEXT,
   CLOSURE_UPDATE_TITLE TEXT,
   CLOSURE_UPDATE_START TEXT
);

CREATE TABLE AnimalViewingAlert (
   SPECIES TEXT NOT NULL,
   EXHIBIT TEXT NOT NULL,
   ALERT_MESSAGE TEXT NOT NULL,
   ALERT_START_DATE TEXT,
   ALERT_END_DATE TEXT,
   PRIMARY KEY (SPECIES, EXHIBIT)
);
"""


def notice(
      title: str,
      description: str,
      start: str,
      end: str | None,
      update_type: str = UpdateType.CLOSURE.value ) -> Update:
   return Update( title, description, update_type, start, end )


def home( species: str, exhibit: str ) -> AnimalSpeciesExhibit:
   return AnimalSpeciesExhibit( species=species, exhibit=exhibit )


def away( species: str, exhibit: str ) -> TemporaryOffDisplayAnimal:
   return TemporaryOffDisplayAnimal(
      species=species,
      exhibit=exhibit,
      viewing_scope='',
      start=date( 2026, 11, 1 ),
      end=date( 2026, 11, 30 ),
      closure_update_title=None,
      closure_update_start=None,
   )


def database( path: Path ) -> None:
   connection = sqlite3.connect( path )
   connection.executescript( SCHEMA )
   connection.commit()
   connection.close()


def insert_closure(
      path: Path,
      title: str,
      description: str,
      start: str,
      end: str | None,
      update_type: str = UpdateType.CLOSURE.value ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO ZooUpdate (
               TITLE, DESCRIPTION, UPDATE_TYPE, START_DATE, END_DATE
            ) VALUES (?, ?, ?, ?, ?)
      """,
      ( title, description, update_type, start, end ),
   )
   connection.commit()
   connection.close()


def insert_home( path: Path, species: str, exhibit: str ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      'INSERT INTO Enclosure ( SPECIES, EXHIBIT ) VALUES (?, ?)',
      ( species, exhibit ),
   )
   connection.commit()
   connection.close()


def insert_away( path: Path, species: str, exhibit: str ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO AnimalStatus (
               SPECIES, EXHIBIT, IS_OFF_DISPLAY, OFF_DISPLAY_FOR_SEASON,
               VIEWING_SCOPE, OFF_DISPLAY_START, OFF_DISPLAY_END,
               CLOSURE_UPDATE_TITLE, CLOSURE_UPDATE_START
            ) VALUES (?, ?, 1, 0, '', '2026-11-01', '2026-11-30', NULL, NULL)
      """,
      ( species, exhibit ),
   )
   connection.commit()
   connection.close()


def insert_alert( path: Path, message: str, end: str ) -> None:
   insert_viewing_alert( path, 'Polar Bear', 'Tundra Trek', message, '2026-07-09', end )


def insert_viewing_alert(
      path: Path,
      species: str,
      exhibit: str,
      message: str,
      start: str,
      end: str | None ) -> None:
   connection = sqlite3.connect( path )
   connection.execute(
      """   INSERT INTO AnimalViewingAlert (
               SPECIES, EXHIBIT, ALERT_MESSAGE, ALERT_START_DATE, ALERT_END_DATE
            ) VALUES (?, ?, ?, ?, ?)
      """,
      ( species, exhibit, message, start, end ),
   )
   connection.commit()
   connection.close()


def stored_alerts( path: Path ) -> list[ tuple[ str, str, str, str | None ] ]:
   connection = sqlite3.connect( path )
   loaded = connection.execute(
      """   SELECT SPECIES, EXHIBIT, ALERT_MESSAGE, ALERT_END_DATE
            FROM AnimalViewingAlert
            ORDER BY SPECIES, EXHIBIT
      """
   ).fetchall()
   connection.close()
   return loaded


def written_sentence(
      cls: type,
      species: str,
      exhibit: str,
      off_display: bool,
      scope: str,
      title: str,
      description: str ) -> str:
   return SENTENCE


def Test_Choose_TestOneHome_ExpectThatExhibit() -> None:
   alerts = ClosureViewingAlert.choose(
      [ notice(
         'The polar bear underwater viewing area is closed.',
         'The pool is still open.',
         '2026-07-09',
         '2026-12-13',
      ) ],
      [ home( 'Polar Bear', 'Tundra Trek' ) ],
      [],
      [],
      TODAY,
   )

   assert len( alerts ) == 1
   assert alerts[ 0 ].exhibit == 'Tundra Trek'
   assert alerts[ 0 ].off_display == False
   assert alerts[ 0 ].replacing == False
   assert alerts[ 0 ].end == date( 2026, 12, 13 )


def Test_Choose_TestFormerHabitat_ExpectCurrentExhibit() -> None:
   alerts = ClosureViewingAlert.choose(
      [ notice(
         'Eurasia Wilds Loop Pathway Closure',
         'A portion of the pathway between the former red panda habitat and the camels is closed due to construction.',
         '2026-11-12',
         '2026-12-13',
      ) ],
      [ home( 'Red Panda', 'Africa Savanna' ) ],
      [],
      [],
      TODAY,
   )

   assert len( alerts ) == 1
   assert alerts[ 0 ].species == 'Red Panda'
   assert alerts[ 0 ].exhibit == 'Africa Savanna'
   assert alerts[ 0 ].off_display == False
   assert alerts[ 0 ].scope == ''


def Test_Choose_TestPluralName_ExpectSpecies() -> None:
   alerts = ClosureViewingAlert.choose(
      [ notice(
         'The polar bears are closed indoors.',
         '',
         '2026-11-13',
         '2026-12-13',
      ) ],
      [ home( 'Polar Bear', 'Tundra Trek' ) ],
      [],
      [],
      TODAY,
   )

   assert [ alert.species for alert in alerts ] == [ 'Polar Bear' ]


def Test_Choose_TestNamedExhibit_ExpectNamedExhibit() -> None:
   alerts = ClosureViewingAlert.choose(
      [ notice(
         'The Tundra Trek polar bear habitat is closed.',
         '',
         '2026-11-13',
         '2026-12-13',
      ) ],
      [
         home( 'Polar Bear', 'Tundra Trek' ),
         home( 'Polar Bear', 'Eurasia Wilds' ),
      ],
      [],
      [],
      TODAY,
   )

   assert [ alert.exhibit for alert in alerts ] == [ 'Tundra Trek' ]


def Test_Choose_TestSeveralHomes_ExpectNoAlert() -> None:
   alerts = ClosureViewingAlert.choose(
      [ notice(
         'The polar bear habitat is closed.',
         '',
         '2026-11-13',
         '2026-12-13',
      ) ],
      [
         home( 'Polar Bear', 'Tundra Trek' ),
         home( 'Polar Bear', 'Eurasia Wilds' ),
      ],
      [],
      [],
      TODAY,
   )

   assert alerts == []


def Test_Choose_TestTemporarilyOffDisplay_ExpectOffDisplayExhibit() -> None:
   alerts = ClosureViewingAlert.choose(
      [ notice(
         'The polar bear habitat is closed.',
         '',
         '2026-11-13',
         '2026-12-13',
      ) ],
      [
         home( 'Polar Bear', 'Tundra Trek' ),
         home( 'Polar Bear', 'Eurasia Wilds' ),
      ],
      [ away( 'Polar Bear', 'Tundra Trek' ) ],
      [],
      TODAY,
   )

   assert len( alerts ) == 1
   assert alerts[ 0 ].exhibit == 'Tundra Trek'
   assert alerts[ 0 ].off_display == True


def Test_Choose_TestLaterClosure_ExpectLaterWindow() -> None:
   alerts = ClosureViewingAlert.choose(
      [
         notice(
            'Indoor viewing is closed.',
            'The polar bear pool is still open.',
            '2026-07-09',
            '2026-11-13',
         ),
         notice(
            'Underwater viewing is closed.',
            'The polar bear can be seen in the pool.',
            '2026-11-13',
            '2026-12-13',
         ),
      ],
      [ home( 'Polar Bear', 'Tundra Trek' ) ],
      [],
      [],
      TODAY,
   )

   assert len( alerts ) == 1
   assert alerts[ 0 ].title == 'Underwater viewing is closed.'
   assert alerts[ 0 ].end == date( 2026, 12, 13 )


def Test_Choose_TestDeparture_ExpectNoAlert() -> None:
   alerts = ClosureViewingAlert.choose(
      [ notice(
         'Pemba the snow leopard is moving to a new zoo.',
         'She can be seen through May 8.',
         '2026-05-02',
         '2026-05-08',
         UpdateType.DEPARTURE.value,
      ) ],
      [ home( 'Snow Leopard', 'Eurasia Wilds' ) ],
      [],
      [],
      TODAY,
   )

   assert alerts == []


def Test_Choose_TestStoredAlert_ExpectReplacing() -> None:
   alerts = ClosureViewingAlert.choose(
      [ notice(
         'The polar bear underwater viewing area is closed.',
         '',
         '2026-07-09',
         '2026-12-13',
      ) ],
      [ home( 'Polar Bear', 'Tundra Trek' ) ],
      [],
      [ AnimalViewingAlert(
         'Polar Bear',
         'Tundra Trek',
         '2026-07-09',
         '2026-12-13',
         'Old sentence.',
      ) ],
      TODAY,
   )

   assert len( alerts ) == 1
   assert alerts[ 0 ].replacing == True


def Test_CheckSchedules_TestClosureNamesAnimal_ExpectAlert(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_home( database_path, 'Polar Bear', 'Tundra Trek' )
   insert_closure(
      database_path,
      'The polar bear underwater viewing area is closed.',
      'The pool is still open.',
      '2026-07-09',
      '2026-12-13',
   )
   monkeypatch.setattr( ViewingAlertSentence, 'write', classmethod( written_sentence ) )
   CheckReport.reset_fixed_count()

   result = ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   assert result == 0
   assert CheckReport.fixed_count == 1
   output = capsys.readouterr().out
   assert 'Set the viewing alert.' in output
   assert SENTENCE in output
   photo = AnimalDetailImage.source( 'Tundra Trek', 'Polar Bear' )

   if ( Paths.ROOT / photo ).is_file():
      assert photo in output
   assert stored_alerts( database_path ) == [
      ( 'Polar Bear', 'Tundra Trek', SENTENCE, '2026-12-13' ),
   ]


def Test_CheckSchedules_TestDifferentSentence_ExpectUpdatedAlert(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_home( database_path, 'Polar Bear', 'Tundra Trek' )
   insert_closure(
      database_path,
      'The polar bear underwater viewing area is closed.',
      'The pool is still open.',
      '2026-07-09',
      '2026-12-13',
   )
   insert_alert( database_path, 'Old sentence.', '2026-12-13' )
   monkeypatch.setattr( ViewingAlertSentence, 'write', classmethod( written_sentence ) )
   CheckReport.reset_fixed_count()

   result = ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   assert result == 0
   assert 'Updated the viewing alert.' in capsys.readouterr().out
   assert stored_alerts( database_path ) == [
      ( 'Polar Bear', 'Tundra Trek', SENTENCE, '2026-12-13' ),
   ]


def Test_CheckSchedules_TestClosureEndsToday_ExpectAlertEndsToday(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_home( database_path, 'Polar Bear', 'Tundra Trek' )
   insert_closure(
      database_path,
      'The polar bear underwater viewing area is closed.',
      'The pool is still open.',
      '2026-07-09',
      '2026-11-13',
   )
   monkeypatch.setattr( ViewingAlertSentence, 'write', classmethod( written_sentence ) )
   CheckReport.reset_fixed_count()

   ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   assert stored_alerts( database_path ) == [
      ( 'Polar Bear', 'Tundra Trek', SENTENCE, '2026-11-13' ),
   ]


def Test_CheckSchedules_TestNoOutsideService_ExpectLocalSentence(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_home( database_path, 'Polar Bear', 'Tundra Trek' )
   insert_closure(
      database_path,
      'The polar bear underwater viewing area is closed.',
      'The pool is still open.',
      '2026-07-09',
      '2026-12-13',
   )
   CheckReport.reset_fixed_count()

   result = ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   sentence = (
      'The polar bear underwater viewing area at Tundra Trek is closed. '
      'The pool is still open.'
   )
   assert result == 0
   assert sentence in capsys.readouterr().out
   assert stored_alerts( database_path ) == [
      ( 'Polar Bear', 'Tundra Trek', sentence, '2026-12-13' ),
   ]


def Test_CheckSchedules_TestSameAlert_ExpectNoRewrite(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_home( database_path, 'Polar Bear', 'Tundra Trek' )
   insert_closure(
      database_path,
      'The polar bear underwater viewing area is closed.',
      'The pool is still open.',
      '2026-07-09',
      '2026-12-13',
   )
   insert_alert( database_path, SENTENCE, '2026-12-13' )
   monkeypatch.setattr( ViewingAlertSentence, 'write', classmethod( written_sentence ) )
   CheckReport.reset_fixed_count()

   result = ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert CheckReport.category_line( 'checks.animalAlerts', 0 ) in capsys.readouterr().out


def Test_CheckSchedules_TestDeparture_ExpectNoAlert(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_home( database_path, 'Snow Leopard', 'Eurasia Wilds' )
   insert_closure(
      database_path,
      'Pemba the snow leopard is moving to a new zoo.',
      'She can be seen through May 8.',
      '2026-05-02',
      '2026-05-08',
      UpdateType.DEPARTURE.value,
   )
   calls: list[ bool ] = []

   def write(
         cls: type,
         species: str,
         exhibit: str,
         off_display: bool,
         scope: str,
         title: str,
         description: str ) -> str:
      calls.append( off_display )
      return SENTENCE

   monkeypatch.setattr( ViewingAlertSentence, 'write', classmethod( write ) )
   CheckReport.reset_fixed_count()

   ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   assert calls == []
   assert stored_alerts( database_path ) == []


def Test_CheckSchedules_TestOffDisplay_ExpectOffDisplayFact(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_home( database_path, 'Polar Bear', 'Tundra Trek' )
   insert_home( database_path, 'Polar Bear', 'Eurasia Wilds' )
   insert_away( database_path, 'Polar Bear', 'Tundra Trek' )
   insert_closure(
      database_path,
      'The polar bear habitat is closed.',
      '',
      '2026-11-13',
      '2026-12-13',
   )
   calls: list[ bool ] = []

   def write(
         cls: type,
         species: str,
         exhibit: str,
         off_display: bool,
         scope: str,
         title: str,
         description: str ) -> str:
      calls.append( off_display )
      return 'The polar bear is temporarily off display at Tundra Trek.'

   monkeypatch.setattr( ViewingAlertSentence, 'write', classmethod( write ) )
   CheckReport.reset_fixed_count()

   ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   assert calls == [ True ]
   assert stored_alerts( database_path ) == [
      (
         'Polar Bear',
         'Tundra Trek',
         'The polar bear is temporarily off display at Tundra Trek.',
         '2026-12-13',
      ),
   ]


def Test_CheckSchedules_TestEndedAlertWithoutClosure_ExpectKept(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_viewing_alert(
      database_path,
      'Snow Leopard',
      'Eurasia Wilds',
      'Pemba is moving to a new zoo.',
      '2026-05-02',
      '2026-05-08',
   )
   CheckReport.reset_fixed_count()

   result = ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   assert result == 0
   assert CheckReport.fixed_count == 0
   assert 'Removed the viewing alert.' not in capsys.readouterr().out
   assert stored_alerts( database_path ) == [
      ( 'Snow Leopard', 'Eurasia Wilds', 'Pemba is moving to a new zoo.', '2026-05-08' ),
   ]


def Test_CheckSchedules_TestActiveAlertWithoutClosure_ExpectRemoved(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   message = 'The polar bears may spend more time off display.'
   insert_viewing_alert(
      database_path,
      'Polar Bear',
      'Tundra Trek',
      message,
      '2026-11-01',
      '2026-12-13',
   )
   CheckReport.reset_fixed_count()

   result = ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   output = capsys.readouterr().out
   photo = AnimalDetailImage.source( 'Tundra Trek', 'Polar Bear' )

   assert result == 0
   assert CheckReport.fixed_count == 1
   assert 'Removed the viewing alert.' in output
   assert message in output
   assert stored_alerts( database_path ) == []

   if ( Paths.ROOT / photo ).is_file():
      assert photo in output


def Test_CheckSchedules_TestClosureBesideUnrelatedAlert_ExpectUnrelatedRemoved(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database_path = tmp_path / 'animals.db'
   database( database_path )
   insert_home( database_path, 'Polar Bear', 'Tundra Trek' )
   insert_closure(
      database_path,
      'The polar bear underwater viewing area is closed.',
      'The pool is still open.',
      '2026-07-09',
      '2026-12-13',
   )
   insert_alert( database_path, SENTENCE, '2026-12-13' )
   message = 'The snow leopards can be seen on Mondays.'
   insert_viewing_alert(
      database_path,
      'Snow Leopard',
      'Eurasia Wilds',
      message,
      '2026-11-01',
      '2026-12-13',
   )
   monkeypatch.setattr( ViewingAlertSentence, 'write', classmethod( written_sentence ) )
   CheckReport.reset_fixed_count()

   result = ClosureViewingAlertChecker.check_schedules( database_path, TODAY )

   output = capsys.readouterr().out

   assert result == 0
   assert CheckReport.fixed_count == 1
   assert 'Removed the viewing alert.' in output
   assert message in output
   assert stored_alerts( database_path ) == [
      ( 'Polar Bear', 'Tundra Trek', SENTENCE, '2026-12-13' ),
   ]
