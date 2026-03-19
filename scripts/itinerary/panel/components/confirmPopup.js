export function showItineraryConfirmPopup({
   title = 'Heads up',
   message = '',
   confirmText = 'Confirm',
   cancelText = 'Cancel',
   onConfirm,
   onCancel,
} = {}) {
   document.querySelector('.tzg-popup.tzg-confirm')?.remove();

   const wrap = document.createElement('div');
   wrap.className = 'tzg-popup tzg-confirm';

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
               <div class="itin-actions-right tzg-popup-actions">
                  <button type="button" class="itin-prev tzg-popup-cancel">${cancelText}</button>
                  <button type="button" class="itin-next tzg-popup-confirm">${confirmText}</button>
               </div>
            </div>
         </section>
      </div>
   `;

   const close = () => wrap.remove();

   const cancel = () => {
      onCancel?.();
      close();
   };

   const confirm = () => {
      onConfirm?.();
      close();
   };

   wrap.querySelector('.itin-overlay')?.addEventListener('click', (e) => {
      if (e.target === e.currentTarget) cancel();
   });

   wrap.querySelector('.tzg-popup-cancel')?.addEventListener('click', cancel);
   wrap.querySelector('.tzg-popup-confirm')?.addEventListener('click', confirm);

   const onKey = (e) => {
      if (e.key === 'Escape') {
         cancel();
         document.removeEventListener('keydown', onKey);
      }
   };
   document.addEventListener('keydown', onKey);

   document.body.appendChild(wrap);

   setTimeout(() => wrap.querySelector('.tzg-popup-confirm')?.focus?.(), 0);
}