from __future__ import annotations

import subprocess
from typing import Any

import pytest

import api.app_strings as app_strings
from api.app_strings import AppStringProvider
from api.html_strings import HtmlStringRenderer


def test_get_app_string_values_reuses_cache_until_sources_change(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   AppStringProvider.clear_cache()
   call_count = 0
   original_run = app_strings.subprocess.run

   def counting_run(
         *args: Any,
         **kwargs: Any ) -> subprocess.CompletedProcess[ str ]:
      nonlocal call_count
      call_count += 1
      return original_run( *args, **kwargs )

   monkeypatch.setattr( app_strings.subprocess, 'run', counting_run )

   first = AppStringProvider.values()
   second = AppStringProvider.values()

   assert first is second
   assert call_count == 1


def test_format_app_string_resolves_guest_status_templates() -> None:
   assert AppStringProvider.format(
      'guestStatus.animals.temporarilyOffDisplay',
      species='Giraffe' ) == 'The Giraffe is temporarily off-display.'


def test_format_app_string_resolves_guest_status_likely_off_display_message() -> None:
   assert AppStringProvider.format(
      'guestStatus.animals.speciesLikelyOffDisplayOnDay',
      species='Giraffe' ) == 'The Giraffe is most likely off display on this day.'


def test_html_string_cache_clear_also_clears_app_string_cache(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   AppStringProvider.clear_cache()
   call_count = 0
   original_run = app_strings.subprocess.run

   def counting_run(
         *args: Any,
         **kwargs: Any ) -> subprocess.CompletedProcess[ str ]:
      nonlocal call_count
      call_count += 1
      return original_run( *args, **kwargs )

   monkeypatch.setattr( app_strings.subprocess, 'run', counting_run )

   AppStringProvider.values()
   HtmlStringRenderer.clear_cache()
   AppStringProvider.values()

   assert call_count == 2
