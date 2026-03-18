export function createWildEncounterSchedulePanelHtml() {
   return `
      <section
         id="wildEncounterSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set Wild Encounter schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="wildEncounterScheduleName"
               >
                  Wild Encounter
               </label>

               <select
                  id="wildEncounterScheduleName"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a Wild Encounter</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="wildEncounterScheduleStartDate"
               >
                  Start date
               </label>

               <input
                  id="wildEncounterScheduleStartDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a start date"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="wildEncounterScheduleEndDate"
               >
                  End date
               </label>

               <input
                  id="wildEncounterScheduleEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to continue until the schedule is ended.
               </div>
            </div>

            <div class="console-operations-field">
               <label class="console-operations-label">
                  Occurs on these days
               </label>

               <div class="console-operations-checkbox-grid">
                  <label class="console-operations-checkbox-option">
                     <input id="wildEncounterScheduleMonday" type="checkbox">
                     <span>Monday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="wildEncounterScheduleTuesday" type="checkbox">
                     <span>Tuesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="wildEncounterScheduleWednesday" type="checkbox">
                     <span>Wednesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="wildEncounterScheduleThursday" type="checkbox">
                     <span>Thursday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="wildEncounterScheduleFriday" type="checkbox">
                     <span>Friday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="wildEncounterScheduleSaturday" type="checkbox">
                     <span>Saturday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="wildEncounterScheduleSunday" type="checkbox">
                     <span>Sunday</span>
                  </label>
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="wildEncounterScheduleTime"
               >
                  Encounter time
               </label>

               <input
                  id="wildEncounterScheduleTime"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an encounter time"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="wildEncounterScheduleMessage"
               >
                  Schedule message
               </label>

               <textarea
                  id="wildEncounterScheduleMessage"
                  class="console-operations-textarea"
                  placeholder="Enter an optional message for this Wild Encounter schedule"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitWildEncounterSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="wildEncounterScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}