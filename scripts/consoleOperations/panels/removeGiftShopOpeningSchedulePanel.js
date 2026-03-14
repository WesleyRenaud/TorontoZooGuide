export function createRemoveGiftShopOpeningSchedulePanelHtml() {
   return `
      <section
         id="removeGiftShopOpeningSchedulePanel"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               Remove gift shop opening schedule
            </h2>
         </div>

         <div class="console-operations-panel-body">

            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="removeGiftShopOpeningScheduleGiftShop"
               >
                  Gift shop
               </label>

               <select
                  id="removeGiftShopOpeningScheduleGiftShop"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">Select a gift shop</option>
               </select>
            </div>

            <div class="console-operations-actions">
               <button
                  id="submitRemoveGiftShopOpeningSchedule"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  Remove
               </button>
            </div>

            <div
               id="removeGiftShopOpeningScheduleStatus"
               class="console-operations-status"
               aria-live="polite"
            ></div>

         </div>

      </section>
   `;
}