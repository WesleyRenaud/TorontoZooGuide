export function createTooltipGlobalListeners({
   tooltipEl,
   isOpen,
   close,
   step,
   getItemAtIndex,
   onAnimalCardClick,
}) {
   let installed = false;

   function getClosest(target, selector) {
      return target?.closest?.(selector) ?? null;
   }

   function handleSpeciesLinkClick(speciesLink, event) {
      event.stopPropagation();

      const externalHref = String(speciesLink.dataset.externalHref ?? '').trim();

      if (externalHref) {
         window.open(externalHref, '_blank');
         return;
      }

      const index = Number(speciesLink.dataset.index);
      const item = getItemAtIndex(index);

      if (item) {
         onAnimalCardClick?.(item);
      }
   }

   function handleDocumentClick(event) {
      const speciesLink = getClosest(event.target, '.species-link');

      if (speciesLink) {
         handleSpeciesLinkClick(speciesLink, event);
         return;
      }

      if (!isOpen()) {
         return;
      }

      const clickedMarker = getClosest(event.target, '.marker');
      const clickedTooltip = tooltipEl?.contains?.(event.target) ?? false;

      if (!clickedMarker && !clickedTooltip) {
         close();
      }
   }

   function handleDocumentKeydown(event) {
      if (!isOpen()) {
         return;
      }

      if (event.key === 'Escape') {
         event.preventDefault();
         close();
         return;
      }

      if (event.key === 'ArrowRight') {
         event.preventDefault();
         step(+1);
         return;
      }

      if (event.key === 'ArrowLeft') {
         event.preventDefault();
         step(-1);
      }
   }

   function install() {
      if (installed) {
         return;
      }

      installed = true;

      document.addEventListener('click', handleDocumentClick);
      document.addEventListener('keydown', handleDocumentKeydown);
   }

   function uninstall() {
      if (!installed) {
         return;
      }

      installed = false;

      document.removeEventListener('click', handleDocumentClick);
      document.removeEventListener('keydown', handleDocumentKeydown);
   }

   return {
      install,
      uninstall,
   };
}
