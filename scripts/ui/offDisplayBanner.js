export function createOffDisplayBanner() {
   let el = null;

   function ensure() {
      if (el) return el;

      el = document.createElement('div');
      el.className = 'off-display-closed-banner';
      el.style.display = 'none';

      el.innerHTML = `
         <div class="off-display-closed-icon">⚠</div>
         <div class="off-display-closed-text"></div>
         <button class="off-display-closed-close" type="button" aria-label="Close">×</button>
      `;

      el.addEventListener('click', (e) => e.stopPropagation());
      el.querySelector('.off-display-closed-close').addEventListener('click', (e) => {
         e.stopPropagation();
         hide();
      });

      document.body.appendChild(el);
      return el;
   }

   function hide() {
      if (!el) return;
      el.style.display = 'none';
   }

   function sync(animal) {
      const messages = [];

      if (animal?.off_display_message) {
         messages.push(animal.off_display_message);
      }

      if (animal?.limited_viewing_message) {
         messages.push(animal.limited_viewing_message);
      }

      if (animal?.viewing_alert_message) {
         messages.push(animal.viewing_alert_message);
      }

      if (messages.length === 0) {
         hide();
         return;
      }

      const uniqueMessages = [...new Set(messages)];

      const banner = ensure();
      banner.querySelector('.off-display-closed-text').innerHTML = uniqueMessages.join('<br><br>');
      banner.style.display = 'flex';
   }

   return { sync, hide };
}