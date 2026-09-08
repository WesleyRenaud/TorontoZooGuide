export class CreateSpeciesLinkTitleHelper {
   static applyLinkDataset(element, dataset = {}) {
      Object.entries(dataset).forEach(([key, value]) => {
         if (value == null) {
            return;
         }

         element.dataset[key] = String(value);
      });
   }

   static bindSpeciesLinkActivation(linkEl, onClick) {
      linkEl.classList.add('species-link');
      linkEl.setAttribute('role', 'button');
      linkEl.setAttribute('tabindex', '0');

      const activate = (event) => {
         event.stopPropagation();
         onClick();
      };

      linkEl.addEventListener('click', activate);
      linkEl.addEventListener('keydown', (event) => {
         if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            activate(event);
         }
      });
   }
}
