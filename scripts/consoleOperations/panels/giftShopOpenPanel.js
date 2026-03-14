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