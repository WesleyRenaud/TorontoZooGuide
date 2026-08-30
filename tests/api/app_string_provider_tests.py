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
   assert AppStringProvider.format(
      'guestStatus.animals.temporarilyOffDisplay',
      species='Giraffe' ) == 'The Giraffe is temporarily off-display.'


def Test_Format_TestLikelyOffDisplayTemplate_ExpectResolvedMessage() -> None:
   assert AppStringProvider.format(
      'guestStatus.animals.speciesLikelyOffDisplayOnDay',
      species='Giraffe' ) == 'The Giraffe is most likely off display on this day.'


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
