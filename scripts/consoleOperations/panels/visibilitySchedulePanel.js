export function createVisibilitySchedulePanelHtml() {
   return `
      <section
         id="visibilitySchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set animal visibility schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="visibilityScheduleExhibit"
               >
                  Exhibit
               </label>

               <select
                  id="visibilityScheduleExhibit"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an exhibit</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="visibilityScheduleSpecies"
               >
                  Species
               </label>

               <input
                  id="visibilityScheduleSpecies"
                  type="text"
                  class="console-operations-input"
                  autocomplete="off"
                  placeholder="Search for a species"
               >

               <div
                  id="visibilityScheduleSpeciesResults"
                  class="console-operations-autocomplete"
               ></div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="visibilityScheduleStartDate"
               >
                  Schedule start date
               </label>

               <input
                  id="visibilityScheduleStartDate"
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
                  for="visibilityScheduleEndDate"
               >
                  Schedule end date
               </label>

               <input
                  id="visibilityScheduleEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep this visibility schedule in place until manually changed.
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="visibilityScheduleDailyStartTime"
               >
                  Daily viewing start time
               </label>

               <input
                  id="visibilityScheduleDailyStartTime"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a daily start time"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="visibilityScheduleDailyEndTime"
               >
                  Daily viewing end time
               </label>

               <input
                  id="visibilityScheduleDailyEndTime"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a daily end time"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="visibilityScheduleMessage"
               >
                  Message
               </label>

               <textarea
                  id="visibilityScheduleMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the viewing message shown to guests"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitVisibilitySchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="visibilityScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}