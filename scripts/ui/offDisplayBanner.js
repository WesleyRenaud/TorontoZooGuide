export function createOffDisplayBanner() {
   let el = null;

   function ensure() {
      if (el) return el;

      el = document.createElement('div');
      el.className = 'off-display-banner';
      el.style.display = 'none';

      el.innerHTML = `
         <div class="off-display-icon">⚠</div>
         <div class="off-display-text"></div>
         <button class="off-display-close" type="button" aria-label="Close">×</button>
      `;

      el.addEventListener('click', (e) => e.stopPropagation());
      el.querySelector('.off-display-close').addEventListener('click', (e) => {
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
      // animals only
      if (!animal?.off_display_message) {
         hide();
         return;
      }
      if (Number(animal.likelihood) !== 0) {
         hide();
         return;
      }

      const banner = ensure();
      banner.querySelector('.off-display-text').innerHTML = animal.off_display_message;
      banner.style.display = 'flex';
   }

   return { sync, hide };
}