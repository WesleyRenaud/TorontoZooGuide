from __future__ import annotations

from pathlib import Path

import pytest

from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_Load_TestValidMembers_ExpectSortedDict(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'sample.json' ).write_text(
      '{\n   "BETA": "beta",\n   "ALPHA": "alpha"\n}\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   assert SharedEnumValues.load( 'sample.json' ) == {
      'ALPHA': 'alpha',
      'BETA': 'beta',
   }


def Test_Load_TestEmptyObject_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'empty.json' ).write_text( '{}\n', encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='non-empty object' ):
      SharedEnumValues.load( 'empty.json' )


def Test_Load_TestInvalidMemberKey_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'bad-key.json' ).write_text(
      '{ "not-valid": "value" }\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='SCREAMING_SNAKE' ):
      SharedEnumValues.load( 'bad-key.json' )


def Test_Load_TestInvalidWireValue_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'bad-value.json' ).write_text(
      '{ "ANIMAL": "" }\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='non-empty string' ):
      SharedEnumValues.load( 'bad-value.json' )


def Test_RepositoryRoot_TestFromModule_ExpectContainsSharedEnums() -> None:
   root = SharedEnumValues.repository_root()

   assert ( root / 'shared' / 'enums' / 'itemType.json' ).is_file()
   assert SharedEnumValues.shared_enums_directory() == root / 'shared' / 'enums'
