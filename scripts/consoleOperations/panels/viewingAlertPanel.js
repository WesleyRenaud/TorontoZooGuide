export function createViewingAlertPanelHtml() {
   return `
      <section
         id="viewingAlertPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set animal viewing alert
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="viewingAlertExhibit"
               >
                  Exhibit
               </label>

               <select
                  id="viewingAlertExhibit"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an exhibit</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="viewingAlertSpecies"
               >
                  Species
               </label>

               <input
                  id="viewingAlertSpecies"
                  type="text"
                  class="console-operations-input"
                  autocomplete="off"
                  placeholder="Search for a species"
               >

               <div
                  id="viewingAlertSpeciesResults"
                  class="console-operations-autocomplete"
               ></div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="viewingAlertStartDate"
               >
                  Start date
               </label>

               <input
                  id="viewingAlertStartDate"
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
                  for="viewingAlertEndDate"
               >
                  End date
               </label>

               <input
                  id="viewingAlertEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep the viewing alert active until manually removed.
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="viewingAlertMessage"
               >
                  Alert message
               </label>

               <textarea
                  id="viewingAlertMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the viewing alert shown to guests"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitViewingAlert"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="viewingAlertStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}