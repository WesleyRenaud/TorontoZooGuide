import { readdirSync, readFileSync, writeFileSync, unlinkSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join( dirname( fileURLToPath( import.meta.url ) ), '../..' );
const DOCS_ROOT = join( ROOT, 'docs/manual-tests' );
const GROUPS = [ 'map', 'itinerary', 'console' ];
const GROUP_LABELS = { map: 'Map', itinerary: 'Itinerary', console: 'Console' };
const STORAGE_KEY = 'tzg.manualTestResults.v1';
const INDEX_PATH = join( DOCS_ROOT, 'index.html' );

const PAGE_CSS = `
:root {
   --mt-bg: #eef1ea;
   --mt-panel: #f7f8f4;
   --mt-ink: #1c2420;
   --mt-muted: #5c6b63;
   --mt-line: #c5cec4;
   --mt-accent: #3d5c45;
   --mt-pass: #2f6b3a;
   --mt-fail: #9b2f2f;
   --mt-blocked: #6b5a2f;
   --mt-pass-bg: #d9eadc;
   --mt-fail-bg: #f3d6d6;
   --mt-blocked-bg: #efe6c9;
}
* { box-sizing: border-box; }
body {
   margin: 0;
   min-height: 100vh;
   font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
   color: var(--mt-ink);
   background:
      radial-gradient(circle at top left, #dfe8d8 0%, transparent 42%),
      linear-gradient(180deg, #f4f6f1 0%, var(--mt-bg) 100%);
}
.top {
   display: flex;
   justify-content: space-between;
   gap: 1.5rem;
   align-items: end;
   padding: 1.25rem 1.5rem;
   border-bottom: 1px solid var(--mt-line);
   background: rgba(247, 248, 244, 0.92);
}
.kicker {
   margin: 0 0 0.2rem;
   text-transform: uppercase;
   letter-spacing: 0.08em;
   font-size: 0.75rem;
   color: var(--mt-muted);
}
.top h1 {
   margin: 0;
   font-size: 1.6rem;
   font-weight: 650;
}
.status {
   margin: 0;
   max-width: 28rem;
   color: var(--mt-muted);
   font-size: 0.95rem;
}
.layout {
   display: grid;
   grid-template-columns: minmax(14rem, 20rem) 1fr;
   min-height: calc(100vh - 5.5rem);
}
.nav {
   padding: 1rem 1rem 2rem;
   border-right: 1px solid var(--mt-line);
   background: var(--mt-panel);
   overflow: auto;
}
.nav h2 {
   margin: 1rem 0 0.4rem;
   font-size: 0.8rem;
   text-transform: uppercase;
   letter-spacing: 0.06em;
   color: var(--mt-muted);
}
.suite-list {
   list-style: none;
   margin: 0;
   padding: 0;
}
.suite-link {
   width: 100%;
   text-align: left;
   border: 1px solid transparent;
   background: transparent;
   color: inherit;
   border-radius: 0.45rem;
   padding: 0.45rem 0.55rem;
   margin-bottom: 0.2rem;
   cursor: pointer;
   font: inherit;
}
.suite-link:hover { background: #e7ece3; }
.suite-link.is-active {
   border-color: var(--mt-accent);
   background: #e2ebdf;
}
.suite-link.is-partial { box-shadow: inset 3px 0 0 var(--mt-blocked); }
.suite-link.is-failed { box-shadow: inset 3px 0 0 var(--mt-fail); }
.suite-link.is-complete { box-shadow: inset 3px 0 0 var(--mt-pass); }
.main {
   padding: 1.25rem 1.5rem 3rem;
   overflow: auto;
}
.suite-header h1 {
   margin: 0 0 0.75rem;
   font-size: 1.45rem;
}
.suite-header p {
   margin: 0.35rem 0;
   line-height: 1.45;
}
.actions {
   display: flex;
   flex-wrap: wrap;
   gap: 0.5rem;
   margin: 1rem 0 0.5rem;
}
.actions button,
.result-btn {
   font: inherit;
   cursor: pointer;
}
.actions button {
   border: 1px solid var(--mt-line);
   background: #fff;
   border-radius: 0.4rem;
   padding: 0.4rem 0.7rem;
}
.summary {
   margin: 0 0 1rem;
   color: var(--mt-muted);
}
.step {
   background: #fff;
   border: 1px solid var(--mt-line);
   border-radius: 0.65rem;
   padding: 0.9rem 1rem 1rem;
   margin-bottom: 0.75rem;
}
.step h2 {
   margin: 0 0 0.55rem;
   font-size: 1.05rem;
}
.step p {
   margin: 0.35rem 0;
   line-height: 1.45;
}
.step.result-pass {
   background: var(--mt-pass-bg);
   border-color: #b7d4bc;
}
.step.result-fail {
   background: var(--mt-fail-bg);
   border-color: #e0b4b4;
}
.step.result-blocked {
   background: var(--mt-blocked-bg);
   border-color: #ddd0a6;
}
.result-row {
   display: flex;
   align-items: center;
   gap: 0.45rem;
   margin: 0.75rem 0 0.5rem;
}
.result-label {
   font-weight: 650;
   margin-right: 0.25rem;
}
.result-btn {
   width: 2.35rem;
   height: 2.35rem;
   border-radius: 999px;
   border: 1.5px solid var(--mt-line);
   background: #fff;
   font-size: 1.15rem;
   line-height: 1;
}
.result-btn.result-pass[aria-pressed="true"] {
   background: var(--mt-pass);
   border-color: var(--mt-pass);
   color: #fff;
}
.result-btn.result-fail[aria-pressed="true"] {
   background: var(--mt-fail);
   border-color: var(--mt-fail);
   color: #fff;
}
.result-btn.result-blocked[aria-pressed="true"] {
   background: var(--mt-blocked);
   border-color: var(--mt-blocked);
   color: #fff;
}
.notes-label {
   display: grid;
   gap: 0.3rem;
   font-weight: 650;
   margin-top: 0.35rem;
}
.notes {
   width: 100%;
   font: inherit;
   border: 1px solid var(--mt-line);
   border-radius: 0.4rem;
   padding: 0.45rem 0.55rem;
   resize: vertical;
   background: rgba(255, 255, 255, 0.85);
}
@media (max-width: 840px) {
   .layout { grid-template-columns: 1fr; }
   .nav {
      border-right: 0;
      border-bottom: 1px solid var(--mt-line);
      max-height: 14rem;
   }
   .top {
      flex-direction: column;
      align-items: start;
   }
}
`.trim();

function loadSuites() {
   const suites = [];
   for ( const group of GROUPS ) {
      const dir = join( DOCS_ROOT, group );
      const names = readdirSync( dir )
         .filter( ( name ) => name.endsWith( '.json' ) )
         .sort();
      for ( const name of names ) {
         const suite = JSON.parse( readFileSync( join( dir, name ), 'utf8' ) );
         if ( !suite.id || !Array.isArray( suite.steps ) ) {
            throw new Error( `Invalid suite JSON: ${group}/${name}` );
         }
         suites.push( { ...suite, group } );
      }
   }
   return suites;
}

function removePerSuiteHtml() {
   let removed = 0;
   for ( const group of GROUPS ) {
      const dir = join( DOCS_ROOT, group );
      for ( const name of readdirSync( dir ) ) {
         if ( !name.endsWith( '.html' ) ) {
            continue;
         }
         unlinkSync( join( dir, name ) );
         removed += 1;
      }
   }
   return removed;
}

function pageScript() {
   return `
(function () {
   var STORAGE_KEY = ${JSON.stringify( STORAGE_KEY )};
   var GROUP_LABELS = ${JSON.stringify( GROUP_LABELS )};
   var GROUPS = ${JSON.stringify( GROUPS )};
   var suites = window.__SUITES__;
   var activeId = null;

   function byId( id ) {
      for ( var i = 0; i < suites.length; i += 1 ) {
         if ( suites[ i ].id === id ) return suites[ i ];
      }
      return null;
   }

   function loadAll() {
      try {
         var raw = localStorage.getItem( STORAGE_KEY );
         return raw ? JSON.parse( raw ) : {};
      } catch ( e ) {
         return {};
      }
   }

   function saveAll( all ) {
      localStorage.setItem( STORAGE_KEY, JSON.stringify( all ) );
   }

   function getSuiteResults( suiteId ) {
      return loadAll()[ suiteId ] || { steps: {} };
   }

   function setStepResult( suiteId, stepNumber, result ) {
      var all = loadAll();
      var saved = all[ suiteId ] || { steps: {} };
      var step = saved.steps[ stepNumber ] || {};
      if ( result ) step.result = result;
      else delete step.result;
      if ( !step.result && !step.notes ) delete saved.steps[ stepNumber ];
      else saved.steps[ stepNumber ] = step;
      all[ suiteId ] = saved;
      saveAll( all );
   }

   function setStepNotes( suiteId, stepNumber, notes ) {
      var all = loadAll();
      var saved = all[ suiteId ] || { steps: {} };
      var step = saved.steps[ stepNumber ] || {};
      step.notes = notes;
      saved.steps[ stepNumber ] = step;
      all[ suiteId ] = saved;
      saveAll( all );
   }

   function clearSuite( suiteId ) {
      var all = loadAll();
      delete all[ suiteId ];
      saveAll( all );
   }

   function escapeHtml( value ) {
      return String( value == null ? '' : value )
         .replace(/&/g, '&amp;')
         .replace(/</g, '&lt;')
         .replace(/>/g, '&gt;')
         .replace(/"/g, '&quot;');
   }

   function applyNavProgress() {
      var buttons = document.querySelectorAll( '.suite-link' );
      for ( var i = 0; i < buttons.length; i += 1 ) {
         var button = buttons[ i ];
         var suite = byId( button.getAttribute( 'data-suite-id' ) );
         button.classList.remove( 'is-complete', 'is-partial', 'is-failed', 'is-active' );
         if ( suite && suite.id === activeId ) button.classList.add( 'is-active' );
         if ( !suite ) continue;
         var saved = getSuiteResults( suite.id );
         var results = [];
         Object.keys( saved.steps || {} ).forEach( function ( key ) {
            if ( saved.steps[ key ].result ) results.push( saved.steps[ key ].result );
         } );
         if ( results.length === 0 ) continue;
         if ( results.indexOf( 'fail' ) !== -1 ) {
            button.classList.add( 'is-failed' );
         } else if ( results.length >= suite.steps.length ) {
            button.classList.add( 'is-complete' );
         } else {
            button.classList.add( 'is-partial' );
         }
      }
   }

   function updateSummary( suite ) {
      var saved = getSuiteResults( suite.id );
      var pass = 0, fail = 0, blocked = 0;
      Object.keys( saved.steps || {} ).forEach( function ( key ) {
         var result = saved.steps[ key ].result;
         if ( result === 'pass' ) pass += 1;
         else if ( result === 'fail' ) fail += 1;
         else if ( result === 'blocked' ) blocked += 1;
      } );
      var answered = pass + fail + blocked;
      document.getElementById( 'summary' ).textContent =
         answered + '/' + suite.steps.length + ' recorded · ' + pass + ' pass · ' + fail + ' fail · ' + blocked + ' blocked';
   }

   function applyStepUi( article, savedStep ) {
      article.classList.remove( 'result-pass', 'result-fail', 'result-blocked' );
      if ( savedStep.result ) article.classList.add( 'result-' + savedStep.result );
      var buttons = article.querySelectorAll( '.result-btn' );
      for ( var i = 0; i < buttons.length; i += 1 ) {
         var btn = buttons[ i ];
         btn.setAttribute(
            'aria-pressed',
            savedStep.result === btn.getAttribute( 'data-result' ) ? 'true' : 'false'
         );
      }
      article.querySelector( '.notes' ).value = savedStep.notes || '';
   }

   function renderSuite( suiteId ) {
      var suite = byId( suiteId );
      if ( !suite ) return;
      activeId = suiteId;
      var saved = getSuiteResults( suite.id );
      var main = document.getElementById( 'main' );
      var html = '';
      html += '<header class="suite-header">';
      html += '<h1>' + escapeHtml( suite.id + ' — ' + suite.title ) + '</h1>';
      var metaFields = [
         { label: 'Preconditions', value: suite.preconditions },
         { label: 'Date under test', value: suite.dateUnderTest },
         { label: 'Cleanup', value: suite.cleanup }
      ];
      for ( var m = 0; m < metaFields.length; m += 1 ) {
         var metaValue = String( metaFields[ m ].value == null ? '' : metaFields[ m ].value ).trim();
         if ( !metaValue || /^none\.?$/i.test( metaValue ) ) {
            continue;
         }
         html += '<p><strong>' + escapeHtml( metaFields[ m ].label ) + ':</strong> '
            + escapeHtml( metaFields[ m ].value ) + '</p>';
      }
      html += '<div class="actions">';
      html += '<button type="button" id="clearResults">Clear suite results</button>';
      html += '<button type="button" id="downloadResults">Download results JSON</button>';
      html += '</div></header>';
      html += '<p id="summary" class="summary"></p>';

      for ( var i = 0; i < suite.steps.length; i += 1 ) {
         var step = suite.steps[ i ];
         html += '<article class="step" data-step="' + step.number + '">';
         html += '<h2>Step ' + step.number + ' — ' + escapeHtml( step.name ) + '</h2>';
         html += '<p><strong>Do:</strong> ' + escapeHtml( step.do ) + '</p>';
         html += '<p><strong>Expect:</strong> ' + escapeHtml( step.expect ) + '</p>';
         html += '<div class="result-row"><span class="result-label">Result:</span>';
         html += '<button type="button" class="result-btn result-pass" data-result="pass" aria-label="Pass" title="Pass" aria-pressed="false">✓</button>';
         html += '<button type="button" class="result-btn result-fail" data-result="fail" aria-label="Fail" title="Fail" aria-pressed="false">✗</button>';
         html += '<button type="button" class="result-btn result-blocked" data-result="blocked" aria-label="Blocked" title="Blocked" aria-pressed="false">◌</button>';
         html += '</div>';
         html += '<label class="notes-label">Notes<textarea class="notes" rows="2" placeholder="Optional notes…"></textarea></label>';
         html += '</article>';
      }
      main.innerHTML = html;

      var articles = main.querySelectorAll( '.step' );
      for ( var a = 0; a < articles.length; a += 1 ) {
         (function ( article ) {
            var stepNumber = Number( article.getAttribute( 'data-step' ) );
            applyStepUi( article, saved.steps[ stepNumber ] || {} );
            var buttons = article.querySelectorAll( '.result-btn' );
            for ( var b = 0; b < buttons.length; b += 1 ) {
               buttons[ b ].addEventListener( 'click', function ( event ) {
                  var value = event.currentTarget.getAttribute( 'data-result' );
                  var current = getSuiteResults( suite.id ).steps[ stepNumber ] || {};
                  var next = current.result === value ? null : value;
                  setStepResult( suite.id, stepNumber, next );
                  applyStepUi( article, getSuiteResults( suite.id ).steps[ stepNumber ] || {} );
                  updateSummary( suite );
                  applyNavProgress();
               } );
            }
            article.querySelector( '.notes' ).addEventListener( 'input', function ( event ) {
               setStepNotes( suite.id, stepNumber, event.target.value );
            } );
         })( articles[ a ] );
      }

      document.getElementById( 'clearResults' ).addEventListener( 'click', function () {
         clearSuite( suite.id );
         renderSuite( suite.id );
      } );

      document.getElementById( 'downloadResults' ).addEventListener( 'click', function () {
         var payload = {
            suiteId: suite.id,
            exportedAt: new Date().toISOString(),
            results: getSuiteResults( suite.id )
         };
         var blob = new Blob( [ JSON.stringify( payload, null, 2 ) ], { type: 'application/json' } );
         var url = URL.createObjectURL( blob );
         var anchor = document.createElement( 'a' );
         anchor.href = url;
         anchor.download = suite.id + '-results.json';
         anchor.click();
         URL.revokeObjectURL( url );
      } );

      updateSummary( suite );
      applyNavProgress();
      document.getElementById( 'status' ).textContent =
         suite.id + ': click ✓ / ✗ / ◌ to record results (saved in this browser).';

      try {
         history.replaceState( {}, '', '#' + encodeURIComponent( suite.id ) );
      } catch ( e ) {}
   }

   function renderNav() {
      var nav = document.getElementById( 'nav' );
      var html = '';
      for ( var g = 0; g < GROUPS.length; g += 1 ) {
         var group = GROUPS[ g ];
         html += '<h2>' + escapeHtml( GROUP_LABELS[ group ] ) + '</h2><ul class="suite-list">';
         for ( var i = 0; i < suites.length; i += 1 ) {
            if ( suites[ i ].group !== group ) continue;
            html += '<li><button type="button" class="suite-link" data-suite-id="' +
               escapeHtml( suites[ i ].id ) + '">' +
               escapeHtml( suites[ i ].id + ' — ' + suites[ i ].title ) +
               '</button></li>';
         }
         html += '</ul>';
      }
      nav.innerHTML = html;
      var buttons = nav.querySelectorAll( '.suite-link' );
      for ( var b = 0; b < buttons.length; b += 1 ) {
         buttons[ b ].addEventListener( 'click', function ( event ) {
            renderSuite( event.currentTarget.getAttribute( 'data-suite-id' ) );
         } );
      }
   }

   renderNav();
   var hashId = ( location.hash || '' ).replace( /^#/, '' );
   var start = byId( decodeURIComponent( hashId ) ) || suites[ 0 ];
   if ( start ) renderSuite( start.id );
})();
`.trim();
}

const suites = loadSuites();
const removed = removePerSuiteHtml();

const html = `<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <title>Manual test runner — Toronto Zoo Guide</title>
   <style>
${PAGE_CSS}
   </style>
</head>
<body>
   <header class="top">
      <div>
         <p class="kicker">Toronto Zoo Guide</p>
         <h1>Manual test runner</h1>
      </div>
      <p id="status" class="status" aria-live="polite"></p>
   </header>
   <div class="layout">
      <nav id="nav" class="nav" aria-label="Test suites"></nav>
      <main id="main" class="main"></main>
   </div>
   <script>
window.__SUITES__ = ${JSON.stringify( suites )};
${pageScript()}
   </script>
</body>
</html>
`;

writeFileSync( INDEX_PATH, html );
console.log( `wrote docs/manual-tests/index.html (${suites.length} suites)` );
console.log( `removed ${removed} per-suite HTML files` );
