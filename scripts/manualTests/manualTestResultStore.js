export class ManualTestResultStore {
   static STORAGE_KEY = 'tzg.manualTestResults.v1';

   static loadAll() {
      try {
         const raw = localStorage.getItem( ManualTestResultStore.STORAGE_KEY );
         return raw ? JSON.parse( raw ) : {};
      } catch {
         return {};
      }
   }

   static saveAll( all ) {
      localStorage.setItem( ManualTestResultStore.STORAGE_KEY, JSON.stringify( all ) );
   }

   static getSuite( suiteId ) {
      return ManualTestResultStore.loadAll()[ suiteId ] || { steps: {} };
   }

   static setStepResult( suiteId, stepNumber, result ) {
      const all = ManualTestResultStore.loadAll();
      const suite = all[ suiteId ] || { steps: {} };
      const step = suite.steps[ stepNumber ] || {};
      if ( result ) {
         step.result = result;
      } else {
         delete step.result;
      }
      if ( !step.result && !step.notes ) {
         delete suite.steps[ stepNumber ];
      } else {
         suite.steps[ stepNumber ] = step;
      }
      all[ suiteId ] = suite;
      ManualTestResultStore.saveAll( all );
   }

   static setStepNotes( suiteId, stepNumber, notes ) {
      const all = ManualTestResultStore.loadAll();
      const suite = all[ suiteId ] || { steps: {} };
      const step = suite.steps[ stepNumber ] || {};
      step.notes = notes;
      suite.steps[ stepNumber ] = step;
      all[ suiteId ] = suite;
      ManualTestResultStore.saveAll( all );
   }

   static clearSuite( suiteId ) {
      const all = ManualTestResultStore.loadAll();
      delete all[ suiteId ];
      ManualTestResultStore.saveAll( all );
   }

   static clearAll() {
      localStorage.removeItem( ManualTestResultStore.STORAGE_KEY );
   }
}
