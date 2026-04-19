export function buildRegionSelectorShell() {
   const root = document.createElement('div');
   root.className = 'itin-overlay';
   root.innerHTML = `
      <section class="itin-card itin-card-tall" role="dialog" aria-modal="true" aria-label="Select regions and exhibits">
         <div class="itin-card-topbar itin-card-topbar-with-close">
            <div class="itin-top-title">Itinerary Builder</div>
            <button class="itin-close" type="button" aria-label="Close itinerary builder">×</button>
         </div>

         <div class="itin-card-body itin-card-body-tall">
            <h1 class="itin-h1">Add Animals by Region</h1>
            <div class="itin-region-results itin-results"></div>
         </div>

         <div class="itin-card-actions-dual">
            <button class="itin-prev" type="button">Back</button>

            <div class="itin-actions-right">
               <button class="itin-next" type="button">Next</button>
               <button class="itin-next itin-finish" type="button">Finish</button>
            </div>
         </div>
      </section>
   `;

   return {
      root,
      resultsEl: root.querySelector('.itin-region-results'),
      prevButton: root.querySelector('.itin-prev'),
      nextButton: root.querySelector('.itin-next'),
      finishButton: root.querySelector('.itin-finish'),
      closeButton: root.querySelector('.itin-close'),
   };
}
