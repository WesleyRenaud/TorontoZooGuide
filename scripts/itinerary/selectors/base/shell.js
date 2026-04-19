export function buildSelectorShell({
   topTitle,
   h1,
   subtitle,
   hideNextButton = false,
} = {}) {
   const root = document.createElement('div');
   root.className = 'itin-overlay';
   root.innerHTML = `
      <section class="itin-card itin-card-tall" role="dialog" aria-modal="true">
         <div class="itin-card-topbar itin-card-topbar-with-close">
            <div class="itin-top-title">${topTitle}</div>
            <button class="itin-close" type="button" aria-label="Close itinerary builder">×</button>
         </div>

         <div class="itin-card-body itin-card-body-tall">
            <h1 class="itin-h1">${h1}</h1>
            <p class="itin-subtitle">${subtitle}</p>

            <input
               class="itin-search-input"
               type="text"
               placeholder="Search..."
               autocomplete="off"
            />

            <div class="itin-results" aria-live="polite"></div>
         </div>

         <div class="itin-card-actions-dual">
            <button class="itin-prev" type="button">Previous</button>

            <div class="itin-actions-right">
               ${hideNextButton ? '' : '<button class="itin-next" type="button">Next</button>'}
               <button class="itin-finish" type="button">Finish</button>
            </div>
         </div>
      </section>
   `;

   return {
      root,
      bodyEl: root.querySelector('.itin-card-body'),
      inputEl: root.querySelector('.itin-search-input'),
      resultsEl: root.querySelector('.itin-results'),
      prevButton: root.querySelector('.itin-prev'),
      nextButton: root.querySelector('.itin-next'),
      finishButton: root.querySelector('.itin-finish'),
      closeButton: root.querySelector('.itin-close'),
   };
}
