import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join( dirname( fileURLToPath( import.meta.url ) ), '../..' );
const DOCS_ROOT = join( ROOT, 'docs/manual-tests' );
const GROUPS = [ 'map', 'itinerary', 'console' ];
const STORAGE_KEY = 'tzg.manualTestResults.v1';

const PAGE_CSS = `
:root {
   --mt-bg: #eef1ea;
   --mt-ink: #1c2420;
   --mt-muted: #5c6b63;
   --mt-line: #c5cec4;
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
.page {
   max-width: 46rem;
   margin: 0 auto;
   padding: 1.25rem 1.25rem 3rem;
}
.kicker {
   margin: 0 0 0.2rem;
   text-transform: uppercase;
   letter-spacing: 0.08em;
   font-size: 0.75rem;
   color: var(--mt-muted);
}
h1 {
   margin: 0 0 0.75rem;
   font-size: 1.45rem;
   font-weight: 650;
}
.meta p {
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
`.trim();

function escapeHtml( value ) {
   return String( value ?? '' )
      .replace( /&/g, '&amp;' )
      .replace( /</g, '&lt;' )
      .replace( />/g, '&gt;' )
      .replace( /"/g, '&quot;' );
}

function renderStepsHtml( steps ) {
   return steps.map( ( step ) => `
      <article class="step" data-step="${step.number}">
         <h2>Step ${step.number} — ${escapeHtml( step.name )}</h2>
         <p><strong>Do:</strong> ${escapeHtml( step.do )}</p>
         <p><strong>Expect:</strong> ${escapeHtml( step.expect )}</p>
         <div class="result-row">
            <span class="result-label">Result:</span>
            <button type="button" class="result-btn result-pass" data-result="pass" aria-label="Pass" title="Pass" aria-pressed="false">✓</button>
            <button type="button" class="result-btn result-fail" data-result="fail" aria-label="Fail" title="Fail" aria-pressed="false">✗</button>
            <button type="button" class="result-btn result-blocked" data-result="blocked" aria-label="Blocked" title="Blocked" aria-pressed="false">◌</button>
         </div>
         <label class="notes-label">Notes
            <textarea class="notes" rows="2" placeholder="Optional notes…"></textarea>
         </label>
      </article>` ).join( '\n' );
}

function pageScript() {
   return `
(function () {
   var STORAGE_KEY = ${JSON.stringify( STORAGE_KEY )};
   var suite = window.__SUITE__;

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

   function getSuite() {
      return loadAll()[ suite.id ] || { steps: {} };
   }

   function setStepResult( stepNumber, result ) {
      var all = loadAll();
      var saved = all[ suite.id ] || { steps: {} };
      var step = saved.steps[ stepNumber ] || {};
      if ( result ) {
         step.result = result;
      } else {
         delete step.result;
      }
      if ( !step.result && !step.notes ) {
         delete saved.steps[ stepNumber ];
      } else {
         saved.steps[ stepNumber ] = step;
      }
      all[ suite.id ] = saved;
      saveAll( all );
   }

   function setStepNotes( stepNumber, notes ) {
      var all = loadAll();
      var saved = all[ suite.id ] || { steps: {} };
      var step = saved.steps[ stepNumber ] || {};
      step.notes = notes;
      saved.steps[ stepNumber ] = step;
      all[ suite.id ] = saved;
      saveAll( all );
   }

   function clearSuite() {
      var all = loadAll();
      delete all[ suite.id ];
      saveAll( all );
   }

   function updateSummary() {
      var saved = getSuite();
      var pass = 0;
      var fail = 0;
      var blocked = 0;
      Object.keys( saved.steps || {} ).forEach( function ( key ) {
         var result = saved.steps[ key ].result;
         if ( result === 'pass' ) pass += 1;
         else if ( result === 'fail' ) fail += 1;
         else if ( result === 'blocked' ) blocked += 1;
      } );
      var total = suite.steps.length;
      var answered = pass + fail + blocked;
      document.getElementById( 'summary' ).textContent =
         answered + '/' + total + ' recorded · ' + pass + ' pass · ' + fail + ' fail · ' + blocked + ' blocked';
   }

   function applyStepUi( article, savedStep ) {
      article.classList.remove( 'result-pass', 'result-fail', 'result-blocked' );
      if ( savedStep.result ) {
         article.classList.add( 'result-' + savedStep.result );
      }
      var buttons = article.querySelectorAll( '.result-btn' );
      for ( var i = 0; i < buttons.length; i += 1 ) {
         var btn = buttons[ i ];
         btn.setAttribute( 'aria-pressed', savedStep.result === btn.getAttribute( 'data-result' ) ? 'true' : 'false' );
      }
      article.querySelector( '.notes' ).value = savedStep.notes || '';
   }

   function bind() {
      var saved = getSuite();
      var articles = document.querySelectorAll( '.step' );
      for ( var i = 0; i < articles.length; i += 1 ) {
         (function ( article ) {
            var stepNumber = Number( article.getAttribute( 'data-step' ) );
            applyStepUi( article, saved.steps[ stepNumber ] || {} );

            var buttons = article.querySelectorAll( '.result-btn' );
            for ( var j = 0; j < buttons.length; j += 1 ) {
               buttons[ j ].addEventListener( 'click', function ( event ) {
                  var value = event.currentTarget.getAttribute( 'data-result' );
                  var current = getSuite().steps[ stepNumber ] || {};
                  var next = current.result === value ? null : value;
                  setStepResult( stepNumber, next );
                  applyStepUi( article, getSuite().steps[ stepNumber ] || {} );
                  updateSummary();
               } );
            }

            article.querySelector( '.notes' ).addEventListener( 'input', function ( event ) {
               setStepNotes( stepNumber, event.target.value );
            } );
         })( articles[ i ] );
      }

      document.getElementById( 'clearResults' ).addEventListener( 'click', function () {
         clearSuite();
         var fresh = getSuite();
         for ( var k = 0; k < articles.length; k += 1 ) {
            applyStepUi( articles[ k ], fresh.steps[ Number( articles[ k ].getAttribute( 'data-step' ) ) ] || {} );
         }
         updateSummary();
      } );

      document.getElementById( 'downloadResults' ).addEventListener( 'click', function () {
         var payload = {
            suiteId: suite.id,
            exportedAt: new Date().toISOString(),
            results: getSuite()
         };
         var blob = new Blob( [ JSON.stringify( payload, null, 2 ) ], { type: 'application/json' } );
         var url = URL.createObjectURL( blob );
         var anchor = document.createElement( 'a' );
         anchor.href = url;
         anchor.download = suite.id + '-results.json';
         anchor.click();
         URL.revokeObjectURL( url );
      } );

      updateSummary();
   }

   bind();
})();
`.trim();
}

function buildPage( suite ) {
   const title = `${suite.id} — ${suite.title}`;
   return `<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <title>${escapeHtml( title )} — Manual test</title>
   <style>
${PAGE_CSS}
   </style>
</head>
<body>
   <div class="page">
      <p class="kicker">Toronto Zoo Guide · Manual test</p>
      <header class="meta">
         <h1>${escapeHtml( title )}</h1>
         <p><strong>Preconditions:</strong> ${escapeHtml( suite.preconditions )}</p>
         <p><strong>Date under test:</strong> ${escapeHtml( suite.dateUnderTest )}</p>
         <p><strong>Cleanup:</strong> ${escapeHtml( suite.cleanup )}</p>
         <div class="actions">
            <button type="button" id="clearResults">Clear suite results</button>
            <button type="button" id="downloadResults">Download results JSON</button>
         </div>
      </header>
      <p id="summary" class="summary"></p>
${renderStepsHtml( suite.steps || [] )}
   </div>
   <script>
window.__SUITE__ = ${JSON.stringify( suite )};
${pageScript()}
   </script>
</body>
</html>
`;
}

function listSuiteJsonFiles() {
   const files = [];
   for ( const group of GROUPS ) {
      const dir = join( DOCS_ROOT, group );
      for ( const name of readdirSync( dir ) ) {
         if ( !name.endsWith( '.json' ) ) {
            continue;
         }
         files.push( join( dir, name ) );
      }
   }
   return files;
}

const suiteFiles = listSuiteJsonFiles();
let written = 0;

for ( const jsonPath of suiteFiles ) {
   const suite = JSON.parse( readFileSync( jsonPath, 'utf8' ) );
   if ( !suite.id || !Array.isArray( suite.steps ) ) {
      throw new Error( `Invalid suite JSON: ${jsonPath}` );
   }
   const htmlPath = jsonPath.replace( /\.json$/, '.html' );
   writeFileSync( htmlPath, buildPage( suite ) );
   written += 1;
   console.log( `wrote ${htmlPath.replace( ROOT + '/', '' )}` );
}

console.log( `Built ${written} suite pages.` );
