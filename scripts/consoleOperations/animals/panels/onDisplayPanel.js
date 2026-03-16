export function createOnDisplayPanelHtml() {
   return `
      <section
         id="onDisplayPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set animal as on display
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="onDisplayExhibit"
               >
                  Exhibit
               </label>

               <select
                  id="onDisplayExhibit"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an exhibit</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="onDisplaySpecies"
               >
                  Species
               </label>

               <input
                  id="onDisplaySpecies"
                  type="text"
                  class="console-operations-input"
                  autocomplete="off"
                  placeholder="Search for a species"
               >

               <div
                  id="onDisplaySpeciesResults"
                  class="console-operations-autocomplete"
               ></div>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitOnDisplay"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="onDisplayStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}