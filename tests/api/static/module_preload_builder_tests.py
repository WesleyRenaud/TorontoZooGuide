from __future__ import annotations

import os
from pathlib import Path
import time

from api.static.module_preload_builder import ModulePreloadBuilder


ANIMALS_ENTRY = './scripts/pages/animalsBootstrap.js'
ANIMALS_PAGE = './pages/animals.html'
ANIMALS_SCRIPT = '<script type="module" src="../scripts/pages/animalsBootstrap.js"></script>'
ANIMALS_ROUTER = '<link rel="modulepreload" href="/scripts/animals/animalsRouter.js">'


def Test_Inject_TestAnimalsPage_ExpectPreloadsRouterBeforeScript() -> None:
   content = Path( ANIMALS_PAGE ).read_text( encoding='utf-8' )

   injected = ModulePreloadBuilder.inject( content, ANIMALS_PAGE )

   assert ANIMALS_ROUTER in injected
   assert injected.index( ANIMALS_ROUTER ) < injected.index( ANIMALS_SCRIPT )


def Test_Inject_TestInlineScript_ExpectNoIndent() -> None:
   content = 'x<script type="module" src="../scripts/pages/animalsBootstrap.js"></script>'

   injected = ModulePreloadBuilder.inject( content, ANIMALS_PAGE )

   assert injected.startswith( 'x<link rel="modulepreload"' )


def Test_Inject_TestNoModule_ExpectSameHtml() -> None:
   content = '<!DOCTYPE html><html></html>'

   assert ModulePreloadBuilder.inject( content, ANIMALS_PAGE ) == content


def Test_UrlsForEntry_TestMissingFile_ExpectEmpty() -> None:
   assert ModulePreloadBuilder.urls_for_entry( './scripts/missing-module.js' ) == []


def Test_UrlsForEntry_TestCalledTwice_ExpectReusesGraph() -> None:
   ModulePreloadBuilder.clear_cache()

   first = ModulePreloadBuilder.urls_for_entry( ANIMALS_ENTRY )
   second = ModulePreloadBuilder.urls_for_entry( ANIMALS_ENTRY )

   assert '/scripts/pages/animalsBootstrap.js' in first
   assert len( first ) == 19
   assert first is second


def Test_UrlsForEntry_TestDynamicImport_ExpectIncludesTarget() -> None:
   ModulePreloadBuilder.clear_cache()

   urls = ModulePreloadBuilder.urls_for_entry( './scripts/mainItineraryBootstrap.js' )

   assert '/scripts/itinerary/wizard/wizardSelectionStepFactory.js' in urls


def Test_UrlsForEntry_TestImportCycle_ExpectEachFileOnce( tmp_path: Path ) -> None:
   first = tmp_path / 'first.js'
   second = tmp_path / 'second.js'
   first.write_text( "import './second.js'\n", encoding='utf-8' )
   second.write_text( "import './first.js'\n", encoding='utf-8' )
   ModulePreloadBuilder.clear_cache()

   urls = ModulePreloadBuilder.urls_for_entry( str( first ) )

   assert len( urls ) == 2


def Test_UrlsForEntry_TestExtensionlessImport_ExpectAddsJs( tmp_path: Path ) -> None:
   entry = tmp_path / 'entry.js'
   dependency = tmp_path / 'dependency.js'
   entry.write_text( 'import "./dependency"\n', encoding='utf-8' )
   dependency.write_text( 'export const value = 1\n', encoding='utf-8' )
   ModulePreloadBuilder.clear_cache()

   urls = ModulePreloadBuilder.urls_for_entry( str( entry ) )

   assert any( url.endswith( '/dependency.js' ) for url in urls )


def Test_UrlsForEntry_TestMissingImport_ExpectSkipsIt( tmp_path: Path ) -> None:
   entry = tmp_path / 'entry.js'
   entry.write_text( "import './missing.js'\n", encoding='utf-8' )
   ModulePreloadBuilder.clear_cache()

   urls = ModulePreloadBuilder.urls_for_entry( str( entry ) )

   assert len( urls ) == 1


def Test_UrlsForEntry_TestChangedFile_ExpectRebuilds( tmp_path: Path ) -> None:
   entry = tmp_path / 'entry.js'
   entry.write_text( 'export const value = 1\n', encoding='utf-8' )
   ModulePreloadBuilder.clear_cache()
   first = ModulePreloadBuilder.urls_for_entry( str( entry ) )
   later = time.time() + 5
   os.utime( entry, ( later, later ) )

   second = ModulePreloadBuilder.urls_for_entry( str( entry ) )

   assert first == second
   assert first is not second
