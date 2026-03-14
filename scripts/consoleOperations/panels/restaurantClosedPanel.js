export function createRestaurantClosedPanelHtml() {
   return `
      <section
         id="restaurantClosedPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set restaurant as closed
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantClosedRestaurant"
               >
                  Restaurant
               </label>

               <select
                  id="restaurantClosedRestaurant"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a restaurant</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantClosedStartDate"
               >
                  Start date
               </label>

               <input
                  id="restaurantClosedStartDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a start date"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantClosedEndDate"
               >
                  End date
               </label>

               <input
                  id="restaurantClosedEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to continue until the restaurant is reopened.
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantClosedMessage"
               >
                  Closed message
               </label>

               <textarea
                  id="restaurantClosedMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the message shown when the restaurant is closed"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitRestaurantClosed"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="restaurantClosedStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}