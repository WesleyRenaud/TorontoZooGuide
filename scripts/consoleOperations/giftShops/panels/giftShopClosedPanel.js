export function createGiftShopClosedPanelHtml() {
   return `
      <section
         id="giftShopClosedPanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Set gift shop as closed
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopClosedGiftShop"
               >
                  Gift shop
               </label>

               <select
                  id="giftShopClosedGiftShop"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a gift shop</option>
               </select>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopClosedStartDate"
               >
                  Start date
               </label>

               <input
                  id="giftShopClosedStartDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select a start date"
                  autocomplete="off"
               >
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopClosedEndDate"
               >
                  End date
               </label>

               <input
                  id="giftShopClosedEndDate"
                  type="text"
                  class="console-operations-input console-operations-datetime"
                  placeholder="Select an end date"
                  autocomplete="off"
               >

               <div class="console-operations-help">
                  Leave blank to continue until the gift shop is reopened.
               </div>
            </div>

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="giftShopClosedMessage"
               >
                  Closed message
               </label>

               <textarea
                  id="giftShopClosedMessage"
                  class="console-operations-textarea"
                  placeholder="Enter the message shown when the gift shop is closed"
               ></textarea>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitGiftShopClosed"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Save
               </button>
            </div>

            <div
               id="giftShopClosedStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}