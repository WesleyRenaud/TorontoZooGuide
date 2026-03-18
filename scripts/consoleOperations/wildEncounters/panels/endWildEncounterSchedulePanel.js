export function createEndWildEncounterSchedulePanelHtml() {
   return `
      <section
         id="endWildEncounterSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               End Wild Encounter schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="endWildEncounterScheduleName"
               >
                  Wild Encounter
               </label>

               <select
                  id="endWildEncounterScheduleName"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a Wild Encounter</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="endWildEncounterScheduleDate"
               >
                  End date
               </label>

               <input
                  id="endWildEncounterScheduleDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select the date the schedule should end"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to end the schedule today.
               </div>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitEndWildEncounterSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="endWildEncounterScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}