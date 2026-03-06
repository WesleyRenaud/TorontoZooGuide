// scripts/pages/itineraryWizard/popup.js
export function showItineraryPopup({
   mountEl,
   title = 'Heads up',
   message = '',
   buttonText = 'OK',
} = {}) {
   if (!mountEl) return;

   mountEl.querySelector('.tzg-popup')?.remove();

   const wrap = document.createElement('div');
   wrap.className = 'tzg-popup';

   wrap.innerHTML = `
      <div class="itin-overlay">
         <section class="itin-card tzg-popup-card" role="dialog" aria-modal="true">
            <div class="itin-card-topbar">
               <div class="itin-top-title">${title}</div>
            </div>

            <div class="itin-card-body tzg-popup-body">
               <div class="tzg-popup-message">${message}</div>
            </div>

            <div class="itin-card-actions">
               <div class="itin-actions-right">
                  <button type="button" class="itin-next tzg-popup-ok">${buttonText}</button>
               </div>
            </div>
         </section>
      </div>
   `;

   const close = () => wrap.remove();

   wrap.querySelector('.itin-overlay')?.addEventListener('click', (e) => {
      if (e.target === e.currentTarget) close();
   });

   wrap.querySelector('.tzg-popup-ok')?.addEventListener('click', close);

   const onKey = (e) => {
      if (e.key === 'Escape') {
         close();
         document.removeEventListener('keydown', onKey);
      }
   };
   document.addEventListener('keydown', onKey);

   mountEl.appendChild(wrap);

   setTimeout(() => wrap.querySelector('.tzg-popup-ok')?.focus?.(), 0);
}