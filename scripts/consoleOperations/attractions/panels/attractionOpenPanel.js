export function createAttractionOpenPanelHtml() {
   return `
      <section
         id="attractionOpenPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set attraction as open
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpenAttraction"
               >
                  Attraction
               </label>

               <select
                  id="attractionOpenAttraction"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an attraction</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpenPreset"
               >
                  Schedule preset
               </label>

               <select
                  id="attractionOpenPreset"
                  class="console-operations-input console-operations-select"
               >
                  <option value="everyDay">Every day</option>
                  <option value="custom">Custom</option>
                  <option value="weekendsOnly">Weekends only</option>
                  <option value="weekendsAndHolidays">Weekends + holidays only</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpenStartDate"
               >
                  Start date
               </label>

               <input
                  id="attractionOpenStartDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a start date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to start immediately.
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpenEndDate"
               >
                  End date
               </label>

               <input
                  id="attractionOpenEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep this schedule active until it is changed.
               </div>
            </div>

            <div class="console-operations-field">
               <label class="console-operations-label">
                  Open on these days
               </label>

               <div class="console-operations-checkbox-grid">
                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpenMonday"
                        type="checkbox"
                     >
                     <span>Monday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpenTuesday"
                        type="checkbox"
                     >
                     <span>Tuesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpenWednesday"
                        type="checkbox"
                     >
                     <span>Wednesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpenThursday"
                        type="checkbox"
                     >
                     <span>Thursday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpenFriday"
                        type="checkbox"
                     >
                     <span>Friday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpenSaturday"
                        type="checkbox"
                     >
                     <span>Saturday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpenSunday"
                        type="checkbox"
                     >
                     <span>Sunday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="attractionOpenHolidaysOnly"
                        type="checkbox"
                     >
                     <span>Holidays</span>
                  </label>
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionOpenMessage"
               >
                  Schedule message
               </label>

               <textarea
                  id="attractionOpenMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the message shown when the attraction is closed outside this schedule"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitAttractionOpen"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="attractionOpenStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}
