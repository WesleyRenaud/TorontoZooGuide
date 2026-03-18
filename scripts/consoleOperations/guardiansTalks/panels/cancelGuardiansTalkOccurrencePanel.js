export function createCancelGuardiansTalkOccurrencePanelHtml() {
   return `
      <section
         id="cancelGuardiansTalkOccurrencePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Cancel Meet the Guardians talk occurrence
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="cancelGuardiansTalkOccurrenceLocation"
               >
                  Location
               </label>

               <select
                  id="cancelGuardiansTalkOccurrenceLocation"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a location</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="cancelGuardiansTalkOccurrenceTalkName"
               >
                  Talk name
               </label>

               <select
                  id="cancelGuardiansTalkOccurrenceTalkName"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a talk</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="cancelGuardiansTalkOccurrenceDate"
               >
                  Date
               </label>

               <select
                  id="cancelGuardiansTalkOccurrenceDate"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a date</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="cancelGuardiansTalkOccurrenceTime"
               >
                  Time
               </label>

               <select
                  id="cancelGuardiansTalkOccurrenceTime"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a time</option>
               </select>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitCancelGuardiansTalkOccurrence"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="cancelGuardiansTalkOccurrenceStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}