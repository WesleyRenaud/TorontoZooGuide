export function createAttractionClosedPanelHtml() {
   return `
      <section
         id="attractionClosedPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set attraction as closed
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionClosedAttraction"
               >
                  Attraction
               </label>

               <select
                  id="attractionClosedAttraction"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select an attraction</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionClosedStartDate"
               >
                  Start date
               </label>

               <input
                  id="attractionClosedStartDate"
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
                  for="attractionClosedEndDate"
               >
                  End date
               </label>

               <input
                  id="attractionClosedEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep the attraction closed until it is manually reopened.
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="attractionClosedMessage"
               >
                  Closure message
               </label>

               <textarea
                  id="attractionClosedMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the closure message shown to guests"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitAttractionClosed"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="attractionClosedStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}