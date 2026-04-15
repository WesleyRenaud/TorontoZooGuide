export function createGiftShopOpenPanelHtml() {
   return `
      <section
         id="giftShopOpenPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set gift shop as open
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopOpenGiftShop"
               >
                  Gift shop
               </label>

               <select
                  id="giftShopOpenGiftShop"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a gift shop</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopOpenPreset"
               >
                  Schedule preset
               </label>

               <select
                  id="giftShopOpenPreset"
                  class="console-operations-input console-operations-select"
               >
                  <option value="everyDay">Every day</option>
                  <option value="custom">Custom</option>
                  <option value="weekendsOnly">Weekends only</option>
                  <option value="weekendsAndHolidays">Weekends + holidays only</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopOpenStartDate"
               >
                  Start date
               </label>

               <input
                  id="giftShopOpenStartDate"
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
                  for="giftShopOpenEndDate"
               >
                  End date
               </label>

               <input
                  id="giftShopOpenEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to keep this schedule active until it is changed.
               </div>
            </div>

            <div class="console-operations-field">
               <label class="console-operations-label">
                  Open on these days
               </label>

               <div class="console-operations-checkbox-grid">
                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpenMonday"
                        type="checkbox"
                     >
                     <span>Monday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpenTuesday"
                        type="checkbox"
                     >
                     <span>Tuesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpenWednesday"
                        type="checkbox"
                     >
                     <span>Wednesday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpenThursday"
                        type="checkbox"
                     >
                     <span>Thursday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpenFriday"
                        type="checkbox"
                     >
                     <span>Friday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpenSaturday"
                        type="checkbox"
                     >
                     <span>Saturday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpenSunday"
                        type="checkbox"
                     >
                     <span>Sunday</span>
                  </label>

                  <label class="console-operations-checkbox-option">
                     <input
                        id="giftShopOpenHolidaysOnly"
                        type="checkbox"
                     >
                     <span>Holidays</span>
                  </label>
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopOpenMessage"
               >
                  Schedule message
               </label>

               <textarea
                  id="giftShopOpenMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the message shown when the gift shop is closed outside this schedule"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitGiftShopOpen"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="giftShopOpenStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}
