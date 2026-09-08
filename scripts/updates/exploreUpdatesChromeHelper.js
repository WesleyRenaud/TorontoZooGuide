export class ExploreUpdatesChromeHelper {
   static createArrowButton({
      label,
      symbol,
      onClick,
   } = {}) {
      const buttonEl = document.createElement('button');
      buttonEl.type = 'button';
      buttonEl.className = 'explore-update-arrow';
      buttonEl.textContent = symbol;
      buttonEl.setAttribute('aria-label', label);
      buttonEl.addEventListener('click', onClick);
      return buttonEl;
   }
}
