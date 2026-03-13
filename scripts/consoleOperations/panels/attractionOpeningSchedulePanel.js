export function createAttractionOpeningSchedulePanelHtml() {
   return `
      <section
         id="attractionOpeningSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set attraction opening schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpeningScheduleAttraction"
               >
                  Attraction
               </label>

               <select
                  id="attractionOpeningScheduleAttraction"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an attraction</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpeningSchedulePreset"
               >
                  Preset
               </label>

               <select
                  id="attractionOpeningSchedulePreset"
                  class="console-operations-input console-operations-select"
               >
                  <option value="custom">Custom</option>
                  <option value="weekendsAndHolidays">Weekends + holidays only</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpeningScheduleStartDate"
               >
                  Start date
               </label>

               <input
                  id="attractionOpeningScheduleStartDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a start date"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpeningScheduleEndDate"
               >
                  End date
               </label>

               <input
                  id="attractionOpeningScheduleEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to continue until the schedule is changed or removed.
               </div>
            </div>

            <div class="console-operations-field">
               <label class="console-operations-label">
                  Open on these days
               </label>

               <div class="console-operations-checkbox-grid">
                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpeningScheduleMonday"
                        type="checkbox"
                     >
                     <span>Monday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpeningScheduleTuesday"
                        type="checkbox"
                     >
                     <span>Tuesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpeningScheduleWednesday"
                        type="checkbox"
                     >
                     <span>Wednesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpeningScheduleThursday"
                        type="checkbox"
                     >
                     <span>Thursday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpeningScheduleFriday"
                        type="checkbox"
                     >
                     <span>Friday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpeningScheduleSaturday"
                        type="checkbox"
                     >
                     <span>Saturday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpeningScheduleSunday"
                        type="checkbox"
                     >
                     <span>Sunday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpeningScheduleHolidaysOnly"
                        type="checkbox"
                     >
                     <span>Holidays</span>
                  </label>
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpeningScheduleMessage"
               >
                  Schedule message
               </label>

               <textarea
                  id="attractionOpeningScheduleMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the message shown when the attraction is closed outside this schedule"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitAttractionOpeningSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="attractionOpeningScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}