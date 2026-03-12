export function createExhibitClosedPanelHtml() {
   return `
      <section
         id="exhibitClosedPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set exhibit as closed
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="exhibitClosedExhibit"
               >
                  Exhibit
               </label>

               <select
                  id="exhibitClosedExhibit"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an exhibit</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="exhibitClosedStartDate"
               >
                  Start date
               </label>

               <input
                  id="exhibitClosedStartDate"
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
                  for="exhibitClosedEndDate"
               >
                  End date
               </label>

               <input
                  id="exhibitClosedEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep the exhibit closed until it is manually reopened.
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="exhibitClosedMessage"
               >
                  Closure message
               </label>

               <textarea
                  id="exhibitClosedMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the closure message shown to guests"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitExhibitClosed"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="exhibitClosedStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}