export function createTooltipGlobalListeners({
   tooltipEl,
   isOpen,
   close,
   step,
   getItemAtIndex,
   onAnimalCardClick,
}) {
   let installed = false;

   function install() {
      if (installed) {
         return;
      }

      installed = true;

      document.addEventListener('click', (e) => {
         const speciesLink = e.target.closest('.species-link');

         if (speciesLink) {
            e.stopPropagation();

            const index = Number(speciesLink.dataset.index);
            const item = getItemAtIndex(index);

            if (item) {
               onAnimalCardClick?.(item);
            }

            return;
         }

         if (!isOpen()) {
            return;
         }

         const clickedMarker = e.target.closest('.marker');
         const clickedTooltip = tooltipEl.contains(e.target);

         if (!clickedMarker && !clickedTooltip) {
            close();
         }
      });

      document.addEventListener('keydown', (e) => {
         if (!isOpen()) {
            return;
         }

         if (e.key === 'Escape') {
            close();
         }

         if (e.key === 'ArrowRight') {
            step(+1);
         }

         if (e.key === 'ArrowLeft') {
            step(-1);
         }
      });
   }

   return { install };
}
