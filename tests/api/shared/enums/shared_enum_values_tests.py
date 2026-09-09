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


def Test_LoadObjectMembers_TestValidMembers_ExpectSortedDict(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'sample.json' ).write_text(
      '{\n'
      '   "BETA": { "kind": "beta", "itemType": "betas", "onboarding": true },\n'
      '   "ALPHA": { "kind": "alpha", "label": "Alpha" }\n'
      '}\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   assert SharedEnumValues.load_object_members( 'sample.json' ) == {
      'ALPHA': { 'kind': 'alpha', 'label': 'Alpha' },
      'BETA': { 'kind': 'beta', 'itemType': 'betas', 'onboarding': True },
   }


def Test_LoadObjectMembers_TestEmptyObject_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'empty.json' ).write_text( '{}\n', encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='non-empty object' ):
      SharedEnumValues.load_object_members( 'empty.json' )


def Test_LoadObjectMembers_TestInvalidMemberKey_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'bad-key.json' ).write_text(
      '{ "not-valid": { "kind": "value" } }\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='SCREAMING_SNAKE' ):
      SharedEnumValues.load_object_members( 'bad-key.json' )


def Test_LoadObjectMembers_TestStringValue_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'string-value.json' ).write_text(
      '{ "ALPHA": "alpha" }\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='must be an object' ):
      SharedEnumValues.load_object_members( 'string-value.json' )


def Test_LoadObjectMembers_TestMissingKind_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'no-kind.json' ).write_text(
      '{ "ALPHA": { "itemType": "alphas" } }\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='kind for ALPHA' ):
      SharedEnumValues.load_object_members( 'no-kind.json' )


def Test_LoadIntegers_TestValidMembers_ExpectSortedDict(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'sample.json' ).write_text(
      '{\n   "SECOND": 1,\n   "FIRST": 0,\n   "LAST": -1\n}\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   assert SharedEnumValues.load_integers( 'sample.json' ) == {
      'FIRST': 0,
      'LAST': -1,
      'SECOND': 1,
   }


def Test_LoadIntegers_TestInvalidValue_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'bad-int.json' ).write_text(
      '{ "FIRST": "0" }\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='integer value' ):
      SharedEnumValues.load_integers( 'bad-int.json' )


def Test_LoadIntegers_TestEmptyObject_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'empty.json' ).write_text( '{}\n', encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='non-empty object' ):
      SharedEnumValues.load_integers( 'empty.json' )


def Test_LoadIntegers_TestInvalidMemberKey_ExpectValueError(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   ( tmp_path / 'bad-key.json' ).write_text(
      '{ "not-valid": 0 }\n',
      encoding='utf-8' )
   monkeypatch.setattr(
      SharedEnumValues,
      'shared_enums_directory',
      staticmethod( lambda: tmp_path ) )

   with pytest.raises( ValueError, match='SCREAMING_SNAKE' ):
      SharedEnumValues.load_integers( 'bad-key.json' )


def Test_RepositoryRoot_TestFromModule_ExpectContainsSharedEnums() -> None:
   root = SharedEnumValues.repository_root()

   assert ( root / 'shared' / 'enums' / 'itemType.json' ).is_file()
   assert SharedEnumValues.shared_enums_directory() == root / 'shared' / 'enums'
