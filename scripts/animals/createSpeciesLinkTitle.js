export function createSpeciesLinkTitleElement({
   text,
   className,
   tagName = 'div',
   onClick = null,
} = {}) {
   const titleEl = document.createElement(tagName);
   titleEl.className = className;
   titleEl.textContent = text;

   if (typeof onClick !== 'function') {
      return titleEl;
   }

   titleEl.classList.add('species-link');
   titleEl.setAttribute('role', 'button');
   titleEl.setAttribute('tabindex', '0');

   const activate = (event) => {
      event.stopPropagation();
      onClick();
   };

   titleEl.addEventListener('click', activate);
   titleEl.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
         event.preventDefault();
         activate(event);
      }
   });

   return titleEl;
}
