export function createGuardiansTalkSchedulePanelHtml() {
   return `
      <section
         id="guardiansTalkSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set Meet the Guardians talk schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="guardiansTalkScheduleLocation"
               >
                  Location
               </label>

               <select
                  id="guardiansTalkScheduleLocation"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an exhibit</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="guardiansTalkScheduleTalkName"
               >
                  Talk name
               </label>

               <select
                  id="guardiansTalkScheduleTalkName"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a talk</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="guardiansTalkScheduleStartDate"
               >
                  Start date
               </label>

               <input
                  id="guardiansTalkScheduleStartDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a start date"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="guardiansTalkScheduleEndDate"
               >
                  End date
               </label>

               <input
                  id="guardiansTalkScheduleEndDate"
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
                     <input id="guardiansTalkScheduleMonday" type="checkbox">
                     <span>Monday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="guardiansTalkScheduleTuesday" type="checkbox">
                     <span>Tuesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="guardiansTalkScheduleWednesday" type="checkbox">
                     <span>Wednesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="guardiansTalkScheduleThursday" type="checkbox">
                     <span>Thursday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="guardiansTalkScheduleFriday" type="checkbox">
                     <span>Friday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="guardiansTalkScheduleSaturday" type="checkbox">
                     <span>Saturday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input id="guardiansTalkScheduleSunday" type="checkbox">
                     <span>Sunday</span>
                  </label>
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="guardiansTalkScheduleTime"
               >
                  Talk time
               </label>

               <input
                  id="guardiansTalkScheduleTime"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a talk time"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="guardiansTalkScheduleMessage"
               >
                  Schedule message
               </label>

               <textarea
                  id="guardiansTalkScheduleMessage"
                  class="console-operations-textarea"
                  placeholder="Enter an optional message for this talk schedule"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitGuardiansTalkSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="guardiansTalkScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}