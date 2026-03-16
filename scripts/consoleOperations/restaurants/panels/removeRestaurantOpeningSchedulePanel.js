export function createRemoveRestaurantOpeningSchedulePanelHtml() {
   return `
      <section
         id="removeRestaurantOpeningSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Remove restaurant opening schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="removeRestaurantOpeningScheduleRestaurant"
               >
                  Restaurant
               </label>

               <select
                  id="removeRestaurantOpeningScheduleRestaurant"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a restaurant</option>
               </select>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitRemoveRestaurantOpeningSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Remove
               </button>
            </div>

            <div
               id="removeRestaurantOpeningScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}