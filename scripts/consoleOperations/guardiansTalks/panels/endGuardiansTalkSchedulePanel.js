export function createEndGuardiansTalkSchedulePanelHtml() {
   return `
      <section
         id="endGuardiansTalkSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               End Meet the Guardians talk schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="endGuardiansTalkScheduleLocation"
               >
                  Location
               </label>

               <select
                  id="endGuardiansTalkScheduleLocation"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a location</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="endGuardiansTalkScheduleTalkName"
               >
                  Talk name
               </label>

               <select
                  id="endGuardiansTalkScheduleTalkName"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a talk</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="endGuardiansTalkScheduleEndDate"
               >
                  End date
               </label>

               <input
                  id="endGuardiansTalkScheduleEndDate"
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
                  id="submitEndGuardiansTalkSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="endGuardiansTalkScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}