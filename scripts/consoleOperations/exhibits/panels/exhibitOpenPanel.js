export function createExhibitOpenPanelHtml() {
   return `
      <section
         id="exhibitOpenPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set exhibit as open
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="exhibitOpenExhibit"
               >
                  Exhibit
               </label>

               <select
                  id="exhibitOpenExhibit"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an exhibit</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="exhibitOpenStartDate"
               >
                  Start date
               </label>

               <input
                  id="exhibitOpenStartDate"
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
                  for="exhibitOpenEndDate"
               >
                  End date
               </label>

               <input
                  id="exhibitOpenEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep the exhibit explicitly open until it is changed.
               </div>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitExhibitOpen"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="exhibitOpenStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}
