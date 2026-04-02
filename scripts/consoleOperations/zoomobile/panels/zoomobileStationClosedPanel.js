export function createZoomobileStationClosedPanelHtml() {
   return `
      <section
         id="zoomobileStationClosedPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set zoomobile station as closed
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="zoomobileStationClosedZoomobileStation"
               >
                  Zoomobile Station
               </label>

               <select
                  id="zoomobileStationClosedZoomobileStation"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a zoomobile station</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="zoomobileStationClosedStartDate"
               >
                  Start date
               </label>

               <input
                  id="zoomobileStationClosedStartDate"
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
                  for="zoomobileStationClosedEndDate"
               >
                  End date
               </label>

               <input
                  id="zoomobileStationClosedEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep the zoomobile station closed until it is manually reopened.
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="zoomobileStationClosedMessage"
               >
                  Closure message
               </label>

               <textarea
                  id="zoomobileStationClosedMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the closure message shown to guests"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitZoomobileStationClosed"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="zoomobileStationClosedStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}