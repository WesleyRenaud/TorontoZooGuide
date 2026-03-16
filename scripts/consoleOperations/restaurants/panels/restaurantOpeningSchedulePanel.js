export function createRestaurantOpeningSchedulePanelHtml() {
   return `
      <section
         id="restaurantOpeningSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set restaurant opening schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantOpeningScheduleRestaurant"
               >
                  Restaurant
               </label>

               <select
                  id="restaurantOpeningScheduleRestaurant"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a restaurant</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantOpeningSchedulePreset"
               >
                  Preset
               </label>

               <select
                  id="restaurantOpeningSchedulePreset"
                  class="console-operations-input console-operations-select"
               >
                  <option value="custom">Custom</option>
                  <option value="weekendsOnly">Weekends only</option>
                  <option value="weekendsAndHolidays">Weekends + holidays only</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantOpeningScheduleStartDate"
               >
                  Start date
               </label>

               <input
                  id="restaurantOpeningScheduleStartDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a start date"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantOpeningScheduleEndDate"
               >
                  End date
               </label>

               <input
                  id="restaurantOpeningScheduleEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to continue until the schedule is changed or removed.
               </div>
            </div>

            <div class="console-operations-field">
               <label class="console-operations-label">
                  Open on these days
               </label>

               <div class="console-operations-checkbox-grid">
                  <label class="console-operations-checkbox-option">
                     <input
                        id="restaurantOpeningScheduleMonday"
                        type="checkbox"
                     >
                     <span>Monday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="restaurantOpeningScheduleTuesday"
                        type="checkbox"
                     >
                     <span>Tuesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="restaurantOpeningScheduleWednesday"
                        type="checkbox"
                     >
                     <span>Wednesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="restaurantOpeningScheduleThursday"
                        type="checkbox"
                     >
                     <span>Thursday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="restaurantOpeningScheduleFriday"
                        type="checkbox"
                     >
                     <span>Friday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="restaurantOpeningScheduleSaturday"
                        type="checkbox"
                     >
                     <span>Saturday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="restaurantOpeningScheduleSunday"
                        type="checkbox"
                     >
                     <span>Sunday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="restaurantOpeningScheduleHolidaysOnly"
                        type="checkbox"
                     >
                     <span>Holidays</span>
                  </label>
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="restaurantOpeningScheduleMessage"
               >
                  Schedule message
               </label>

               <textarea
                  id="restaurantOpeningScheduleMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the message shown when the restaurant is closed outside this schedule"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitRestaurantOpeningSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="restaurantOpeningScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}