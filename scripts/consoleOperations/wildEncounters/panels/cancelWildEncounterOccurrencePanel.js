export function createCancelWildEncounterOccurrencePanelHtml() {
   return `
      <section
         id="cancelWildEncounterOccurrencePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Cancel Wild Encounter occurrence
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="cancelWildEncounterOccurrenceName"
               >
                  Wild Encounter
               </label>

               <select
                  id="cancelWildEncounterOccurrenceName"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a Wild Encounter</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="cancelWildEncounterOccurrenceDate"
               >
                  Date
               </label>

               <select
                  id="cancelWildEncounterOccurrenceDate"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a date</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="cancelWildEncounterOccurrenceTime"
               >
                  Time
               </label>

               <select
                  id="cancelWildEncounterOccurrenceTime"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a time</option>
               </select>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitCancelWildEncounterOccurrence"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="cancelWildEncounterOccurrenceStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}