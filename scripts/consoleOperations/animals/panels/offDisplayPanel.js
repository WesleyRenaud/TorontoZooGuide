export function createOffDisplayPanelHtml() {
   return `
      <section
         id="offDisplayPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set animal as off display
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="offDisplayExhibit"
               >
                  Exhibit
               </label>

               <select
                  id="offDisplayExhibit"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an exhibit</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="offDisplaySpecies"
               >
                  Species
               </label>

               <input
                  id="offDisplaySpecies"
                  type="text"
                  class="console-operations-input"
                  autocomplete="off"
                  placeholder="Search for a species"
               >

               <div
                  id="offDisplaySpeciesResults"
                  class="console-operations-autocomplete"
               ></div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="offDisplayStartDate"
               >
                  Start date
               </label>

               <input
                  id="offDisplayStartDate"
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
                  for="offDisplayEndDate"
               >
                  End date
               </label>

               <input
                  id="offDisplayEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep the animal off display until it is manually set back on display.
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="offDisplayMessage"
               >
                  Reason
               </label>

               <textarea
                  id="offDisplayMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the reason this animal is off display"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitOffDisplay"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="offDisplayStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}