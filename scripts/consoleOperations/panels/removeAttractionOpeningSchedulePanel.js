export function createRemoveAttractionOpeningSchedulePanelHtml() {
   return `
      <section
         id="removeAttractionOpeningSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Remove attraction opening schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="removeAttractionOpeningScheduleAttraction"
               >
                  Attraction
               </label>

               <select
                  id="removeAttractionOpeningScheduleAttraction"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an attraction</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="removeAttractionOpeningScheduleStartDate"
               >
                  Schedule start date
               </label>

               <input
                  id="removeAttractionOpeningScheduleStartDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select the schedule start date"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitRemoveAttractionOpeningSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Remove
               </button>
            </div>

            <div
               id="removeAttractionOpeningScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}