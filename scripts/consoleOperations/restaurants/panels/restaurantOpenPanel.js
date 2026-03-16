export function createRestaurantOpenPanelHtml() {
   return `
      <section
         id="restaurantOpenPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set restaurant as open
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantOpenRestaurant"
               >
                  Restaurant
               </label>

               <select
                  id="restaurantOpenRestaurant"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a restaurant</option>
               </select>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitRestaurantOpen"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="restaurantOpenStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}