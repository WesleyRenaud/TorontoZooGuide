export function createGiftShopOpeningSchedulePanelHtml() {
   return `
      <section
         id="giftShopOpeningSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set gift shop opening schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopOpeningScheduleGiftShop"
               >
                  Gift Shop
               </label>

               <select
                  id="giftShopOpeningScheduleGiftShop"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a gift shop</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopOpeningSchedulePreset"
               >
                  Preset
               </label>

               <select
                  id="giftShopOpeningSchedulePreset"
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
                  for="giftShopOpeningScheduleStartDate"
               >
                  Start date
               </label>

               <input
                  id="giftShopOpeningScheduleStartDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a start date"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopOpeningScheduleEndDate"
               >
                  End date
               </label>

               <input
                  id="giftShopOpeningScheduleEndDate"
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
                        id="giftShopOpeningScheduleMonday"
                        type="checkbox"
                     >
                     <span>Monday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpeningScheduleTuesday"
                        type="checkbox"
                     >
                     <span>Tuesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpeningScheduleWednesday"
                        type="checkbox"
                     >
                     <span>Wednesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpeningScheduleThursday"
                        type="checkbox"
                     >
                     <span>Thursday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpeningScheduleFriday"
                        type="checkbox"
                     >
                     <span>Friday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpeningScheduleSaturday"
                        type="checkbox"
                     >
                     <span>Saturday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpeningScheduleSunday"
                        type="checkbox"
                     >
                     <span>Sunday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpeningScheduleHolidaysOnly"
                        type="checkbox"
                     >
                     <span>Holidays</span>
                  </label>
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopOpeningScheduleMessage"
               >
                  Schedule message
               </label>

               <textarea
                  id="giftShopOpeningScheduleMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the message shown when the gift shop is closed outside this schedule"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitGiftShopOpeningSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="giftShopOpeningScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}