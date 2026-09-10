import { SuiteManifest } from './suiteManifest.js';
import { ManualTestResultStore } from './manualTestResultStore.js';

export class ManualTestRunner {
   constructor({
      suiteListEl,
      suiteViewEl,
      statusEl,
   }) {
      this.suiteListEl = suiteListEl;
      this.suiteViewEl = suiteViewEl;
      this.statusEl = statusEl;
      this.activeSuiteId = null;
   }

   start() {
      this.renderSuiteList();
      const params = new URLSearchParams( window.location.search );
      const suiteId = params.get( 'suite' ) || SuiteManifest.SUITES[ 0 ]?.id;
      if ( suiteId ) {
         this.openSuite( suiteId );
      }
   }

   renderSuiteList() {
      const groups = [ 'map', 'itinerary', 'console' ];
      this.suiteListEl.replaceChildren();

      for ( const group of groups ) {
         const heading = document.createElement( 'h2' );
         heading.textContent = SuiteManifest.GROUP_LABELS[ group ];
         this.suiteListEl.append( heading );

         const list = document.createElement( 'ul' );
         list.className = 'manual-test-suite-list';

         for ( const suite of SuiteManifest.SUITES.filter( ( item ) => item.group === group ) ) {
            const li = document.createElement( 'li' );
            const button = document.createElement( 'button' );
            button.type = 'button';
            button.className = 'manual-test-suite-link';
            button.dataset.suiteId = suite.id;
            button.textContent = `${suite.id} — ${suite.title}`;
            this.applySuiteProgressClass( button, suite.id );
            button.addEventListener( 'click', () => this.openSuite( suite.id ) );
            li.append( button );
            list.append( li );
         }

         this.suiteListEl.append( list );
      }
   }

   applySuiteProgressClass( button, suiteId, totalSteps = null ) {
      button.classList.remove( 'is-complete', 'is-partial', 'is-failed' );
      const saved = ManualTestResultStore.getSuite( suiteId );
      const results = Object.values( saved.steps || {} )
         .map( ( step ) => step.result )
         .filter( Boolean );
      if ( results.length === 0 ) {
         return;
      }
      if ( results.includes( 'fail' ) ) {
         button.classList.add( 'is-failed' );
         return;
      }
      if ( totalSteps != null && results.length >= totalSteps ) {
         button.classList.add( 'is-complete' );
         return;
      }
      button.classList.add( 'is-partial' );
   }

   updateNavProgress( suiteId ) {
      const button = this.suiteListEl.querySelector( `[data-suite-id="${suiteId}"]` );
      if ( !button ) {
         return;
      }
      const totalSteps = this.suiteViewEl.querySelectorAll( '.manual-test-step' ).length;
      this.applySuiteProgressClass( button, suiteId, totalSteps || null );
      this.highlightActiveSuite( suiteId );
   }

   async openSuite( suiteId ) {
      const suite = SuiteManifest.SUITES.find( ( item ) => item.id === suiteId );
      if ( !suite ) {
         this.setStatus( `Unknown suite: ${suiteId}` );
         return;
      }

      this.activeSuiteId = suiteId;
      this.setStatus( `Loading ${suiteId}…` );
      this.highlightActiveSuite( suiteId );

      const url = new URL( window.location.href );
      url.searchParams.set( 'suite', suiteId );
      window.history.replaceState( {}, '', url );

      try {
         const response = await fetch( suite.path );
         if ( !response.ok ) {
            throw new Error( `HTTP ${response.status}` );
         }
         const data = await response.json();
         this.renderSuite( suite, data );
         this.setStatus( `${suiteId}: click ✓ / ✗ / ◌ to record results (saved in this browser).` );
      } catch ( error ) {
         this.suiteViewEl.replaceChildren();
         const message = document.createElement( 'p' );
         message.className = 'manual-test-error';
         message.textContent = `Could not load ${suite.path}: ${error.message}. Ensure the server is running (npm start).`;
         this.suiteViewEl.append( message );
         this.setStatus( 'Load failed' );
      }
   }

   highlightActiveSuite( suiteId ) {
      for ( const button of this.suiteListEl.querySelectorAll( '.manual-test-suite-link' ) ) {
         button.classList.toggle( 'is-active', button.dataset.suiteId === suiteId );
      }
   }

   renderSuite( suite, data ) {
      const saved = ManualTestResultStore.getSuite( suite.id );
      this.suiteViewEl.replaceChildren();

      const header = document.createElement( 'header' );
      header.className = 'manual-test-suite-header';

      const title = document.createElement( 'h1' );
      title.textContent = data.id && data.title
         ? `${data.id} — ${data.title}`
         : ( data.title || `${suite.id} — ${suite.title}` );
      header.append( title );

      for ( const [ key, labelText ] of [
         [ 'preconditions', 'Preconditions' ],
         [ 'dateUnderTest', 'Date under test' ],
         [ 'cleanup', 'Cleanup' ],
      ] ) {
         if ( !data[ key ] ) {
            continue;
         }
         const row = document.createElement( 'p' );
         const label = document.createElement( 'strong' );
         label.textContent = `${labelText}: `;
         row.append( label, document.createTextNode( data[ key ] ) );
         header.append( row );
      }

      const actions = document.createElement( 'div' );
      actions.className = 'manual-test-suite-actions';

      const clearButton = document.createElement( 'button' );
      clearButton.type = 'button';
      clearButton.textContent = 'Clear suite results';
      clearButton.addEventListener( 'click', () => {
         ManualTestResultStore.clearSuite( suite.id );
         this.renderSuite( suite, data );
      } );

      const exportButton = document.createElement( 'button' );
      exportButton.type = 'button';
      exportButton.textContent = 'Download results JSON';
      exportButton.addEventListener( 'click', () => this.downloadResults( suite.id ) );

      actions.append( clearButton, exportButton );
      header.append( actions );
      this.suiteViewEl.append( header );

      const summary = document.createElement( 'p' );
      summary.className = 'manual-test-summary';
      summary.dataset.summaryFor = suite.id;
      this.suiteViewEl.append( summary );

      const steps = data.steps || [];
      for ( const step of steps ) {
         this.suiteViewEl.append( this.buildStepCard( suite.id, step, saved.steps[ step.number ] || {} ) );
      }

      this.updateSummary( suite.id, steps.length );
      this.updateNavProgress( suite.id );
   }

   buildStepCard( suiteId, step, savedStep ) {
      const article = document.createElement( 'article' );
      article.className = 'manual-test-step';
      article.dataset.step = String( step.number );
      if ( savedStep.result ) {
         article.classList.add( `result-${savedStep.result}` );
      }

      const heading = document.createElement( 'h2' );
      heading.textContent = `Step ${step.number} — ${step.name}`;
      article.append( heading );

      const doLine = document.createElement( 'p' );
      const doLabel = document.createElement( 'strong' );
      doLabel.textContent = 'Do: ';
      doLine.append( doLabel, document.createTextNode( step.do ) );
      article.append( doLine );

      const expectLine = document.createElement( 'p' );
      const expectLabel = document.createElement( 'strong' );
      expectLabel.textContent = 'Expect: ';
      expectLine.append( expectLabel, document.createTextNode( step.expect ) );
      article.append( expectLine );

      const resultRow = document.createElement( 'div' );
      resultRow.className = 'manual-test-result-row';
      const resultLabel = document.createElement( 'span' );
      resultLabel.className = 'manual-test-result-label';
      resultLabel.textContent = 'Result:';
      resultRow.append( resultLabel );

      for ( const { value, symbol, aria } of [
         { value: 'pass', symbol: '✓', aria: 'Pass' },
         { value: 'fail', symbol: '✗', aria: 'Fail' },
         { value: 'blocked', symbol: '◌', aria: 'Blocked' },
      ] ) {
         const button = document.createElement( 'button' );
         button.type = 'button';
         button.className = `manual-test-result-btn result-${value}`;
         button.textContent = symbol;
         button.setAttribute( 'aria-label', aria );
         button.title = aria;
         button.setAttribute( 'aria-pressed', savedStep.result === value ? 'true' : 'false' );
         button.addEventListener( 'click', () => {
            const current = ManualTestResultStore.getSuite( suiteId ).steps[ step.number ] || {};
            const next = current.result === value ? null : value;
            ManualTestResultStore.setStepResult( suiteId, step.number, next );
            const refreshed = ManualTestResultStore.getSuite( suiteId ).steps[ step.number ] || {};
            article.classList.remove( 'result-pass', 'result-fail', 'result-blocked' );
            if ( refreshed.result ) {
               article.classList.add( `result-${refreshed.result}` );
            }
            for ( const peer of resultRow.querySelectorAll( '.manual-test-result-btn' ) ) {
               const peerValue = [ 'pass', 'fail', 'blocked' ].find( ( item ) =>
                  peer.classList.contains( `result-${item}` ) );
               peer.setAttribute( 'aria-pressed', refreshed.result === peerValue ? 'true' : 'false' );
            }
            savedStep.result = refreshed.result;
            this.updateSummary( suiteId, this.suiteViewEl.querySelectorAll( '.manual-test-step' ).length );
            this.updateNavProgress( suiteId );
         } );
         resultRow.append( button );
      }

      article.append( resultRow );

      const notesLabel = document.createElement( 'label' );
      notesLabel.className = 'manual-test-notes-label';
      notesLabel.textContent = 'Notes';
      const notes = document.createElement( 'textarea' );
      notes.className = 'manual-test-notes';
      notes.rows = 2;
      notes.placeholder = 'Optional notes…';
      notes.value = savedStep.notes || '';
      notes.addEventListener( 'input', () => {
         ManualTestResultStore.setStepNotes( suiteId, step.number, notes.value );
      } );
      notesLabel.append( notes );
      article.append( notesLabel );

      return article;
   }

   updateSummary( suiteId, totalSteps ) {
      const summary = this.suiteViewEl.querySelector( '[data-summary-for]' );
      if ( !summary ) {
         return;
      }
      const saved = ManualTestResultStore.getSuite( suiteId );
      let pass = 0;
      let fail = 0;
      let blocked = 0;
      for ( const step of Object.values( saved.steps || {} ) ) {
         if ( step.result === 'pass' ) {
            pass += 1;
         } else if ( step.result === 'fail' ) {
            fail += 1;
         } else if ( step.result === 'blocked' ) {
            blocked += 1;
         }
      }
      const answered = pass + fail + blocked;
      summary.textContent = `${answered}/${totalSteps} recorded · ${pass} pass · ${fail} fail · ${blocked} blocked`;
   }

   downloadResults( suiteId ) {
      const payload = {
         suiteId,
         exportedAt: new Date().toISOString(),
         results: ManualTestResultStore.getSuite( suiteId ),
      };
      const blob = new Blob( [ JSON.stringify( payload, null, 2 ) ], { type: 'application/json' } );
      const url = URL.createObjectURL( blob );
      const anchor = document.createElement( 'a' );
      anchor.href = url;
      anchor.download = `${suiteId}-results.json`;
      anchor.click();
      URL.revokeObjectURL( url );
   }

   setStatus( text ) {
      this.statusEl.textContent = text;
   }
}
