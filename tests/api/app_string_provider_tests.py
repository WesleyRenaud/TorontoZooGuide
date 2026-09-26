from __future__ import annotations

import subprocess
from typing import Any

import pytest

import api.app_string_provider as app_string_provider
from api.app_string_provider import AppStringProvider
from api.html_string_renderer import HtmlStringRenderer


def Test_Values_TestRepeatedCalls_ExpectReusesCacheUntilSourcesChange(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   AppStringProvider.clear_cache()
   call_count = 0
   original_run = app_string_provider.subprocess.run

   def counting_run(
         *args: Any,
         **kwargs: Any ) -> subprocess.CompletedProcess[ str ]:
      nonlocal call_count
      call_count += 1
      return original_run( *args, **kwargs )

   monkeypatch.setattr( app_string_provider.subprocess, 'run', counting_run )

   first = AppStringProvider.values()
   second = AppStringProvider.values()

   assert first is second
   assert call_count == 1


def Test_Format_TestGuestStatusTemplate_ExpectResolvedMessage() -> None:
   species = 'Giraffe'
   key = 'guestStatus.animals.temporarilyOffDisplay'
   template = AppStringProvider.values()[ key ]

   message = AppStringProvider.format( key, species=species )

   assert message == template.format( species=species )


def Test_Format_TestUnknownKey_ExpectKeyError() -> None:
   key = 'missing.key'

   with pytest.raises( KeyError, match=key ):
      AppStringProvider.format( key )


def Test_Format_TestLikelyOffDisplayTemplate_ExpectResolvedMessage() -> None:
   species = 'Giraffe'
   key = 'guestStatus.animals.speciesLikelyOffDisplayOnDay'
   template = AppStringProvider.values()[ key ]

   message = AppStringProvider.format( key, species=species )

   assert message == template.format( species=species )


def Test_ClearCache_TestHtmlStringCacheClear_ExpectAlsoClearsAppStringCache(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   AppStringProvider.clear_cache()
   call_count = 0
   original_run = app_string_provider.subprocess.run

   def counting_run(
         *args: Any,
         **kwargs: Any ) -> subprocess.CompletedProcess[ str ]:
      nonlocal call_count
      call_count += 1
      return original_run( *args, **kwargs )

   monkeypatch.setattr( app_string_provider.subprocess, 'run', counting_run )

   AppStringProvider.values()
   HtmlStringRenderer.clear_cache()
   AppStringProvider.values()

   assert call_count == 2
