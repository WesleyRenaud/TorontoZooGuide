export function createRemoveViewingAlertPanelHtml() {
   return `
      <section
         id="removeViewingAlertPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Remove animal viewing alert
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="removeViewingAlertExhibit"
               >
                  Exhibit
               </label>

               <select
                  id="removeViewingAlertExhibit"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an exhibit</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="removeViewingAlertSpecies"
               >
                  Species
               </label>

               <input
                  id="removeViewingAlertSpecies"
                  type="text"
                  class="console-operations-input"
                  autocomplete="off"
                  placeholder="Search for a species"
               >

               <div
                  id="removeViewingAlertSpeciesResults"
                  class="console-operations-autocomplete"
               ></div>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitRemoveViewingAlert"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Remove alert
               </button>
            </div>

            <div
               id="removeViewingAlertStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}