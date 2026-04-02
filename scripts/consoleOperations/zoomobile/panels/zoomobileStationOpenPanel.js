export function createZoomobileStationOpenPanelHtml() {
   return `
      <section
         id="zoomobileStationOpenPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set zoomobile station as open
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="zoomobileStationOpenZoomobileStation"
               >
                  Zoomobile Station
               </label>

               <select
                  id="zoomobileStationOpenZoomobileStation"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a zoomobile station</option>
               </select>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitZoomobileStationOpen"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="zoomobileStationOpenStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}