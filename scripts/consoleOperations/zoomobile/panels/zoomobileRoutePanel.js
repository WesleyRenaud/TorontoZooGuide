export function createZoomobileRoutePanelHtml() {
   return `
      <section
         id="zoomobileRoutePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set current Zoomobile route
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label class="console-operations-label">
                  Route
               </label>

               <div class="console-operations-radio-group">
                  <label class="console-operations-radio-option">
                     <input
                        id="zoomobileRouteSummer"
                        name="zoomobileRoute"
                        type="radio"
                        value="summer"
                     >
                     <span>Summer</span>
                  </label>

                  <label class="console-operations-radio-option">
                     <input
                        id="zoomobileRouteWinter"
                        name="zoomobileRoute"
                        type="radio"
                        value="winter"
                     >
                     <span>Winter</span>
                  </label>
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="zoomobileRouteStartDate"
               >
                  Start date
               </label>

               <input
                  id="zoomobileRouteStartDate"
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
                  for="zoomobileRouteEndDate"
               >
                  End date
               </label>

               <input
                  id="zoomobileRouteEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep this route until it is changed again.
               </div>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitZoomobileRoute"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="zoomobileRouteStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}
