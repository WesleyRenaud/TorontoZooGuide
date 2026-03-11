export function createRemoveVisibilitySchedulePanelHtml() {
   return `
      <section
         id="removeVisibilitySchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Remove visibility schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="removeVisibilityScheduleExhibit"
               >
                  Exhibit
               </label>

               <select
                  id="removeVisibilityScheduleExhibit"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an exhibit</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="removeVisibilityScheduleSpecies"
               >
                  Species
               </label>

               <input
                  id="removeVisibilityScheduleSpecies"
                  type="text"
                  class="console-operations-input"
                  autocomplete="off"
                  placeholder="Search for a species"
               >

               <div
                  id="removeVisibilityScheduleSpeciesResults"
                  class="console-operations-autocomplete"
               ></div>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitRemoveVisibilitySchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="removeVisibilityScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}