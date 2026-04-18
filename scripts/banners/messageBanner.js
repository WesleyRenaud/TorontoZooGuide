export function createMessageBanner({
   getMessages = () => [],
} = {}) {
   let element = null;

   function ensure() {
      if (element) return element;

      element = document.createElement('div');
      element.className = 'off-display-closed-banner';
      element.style.display = 'none';

      element.innerHTML = `
         <div class="off-display-closed-icon">⚠</div>
         <div class="off-display-closed-text"></div>
         <button class="off-display-closed-close" type="button" aria-label="Close">×</button>
      `;

      element.addEventListener('click', event => event.stopPropagation());
      element.querySelector('.off-display-closed-close').addEventListener('click', event => {
         event.stopPropagation();
         hide();
      });

      document.body.appendChild(element);

      return element;
   }

   function hide() {
      if (!element) return;
      element.style.display = 'none';
   }

   function sync(item) {
      const messages = getMessages(item);

      if (!messages.length) {
         hide();
         return;
      }

      const banner = ensure();
      banner.querySelector('.off-display-closed-text').innerHTML = messages.join('<br><br>');
      banner.style.display = 'flex';
   }

   return { sync, hide };
}
