export function createAttractionClosedBanner() {
   let el = null;

   function ensure() {
      if(el) return el;

      el = document.createElement('div');
      el.className = 'attraction-closed-banner';
      el.style.display = 'none';

      el.innerHTML = `
         <div class="attraction-closed-icon">⚠</div>
         <div class="attraction-closed-text"></div>
         <button class="attraction-closed-close" type="button" aria-label="Close">×</button>
      `;

      el.addEventListener('click', (e) => e.stopPropagation());
      el.querySelector('.attraction-closed-close').addEventListener('click', (e) => {
         e.stopPropagation();
         hide();
      });

      document.body.appendChild(el);
      return el;
   }

   function hide() {
      if(!el) return;
      el.style.display = 'none';
   }

   function sync(attraction) {
      const message = attraction?.closed_message;

      if(!message) {
         hide();
         return;
      }

      const banner = ensure();
      banner.querySelector('.attraction-closed-text').innerHTML = message;
      banner.style.display = 'flex';
   }

   return { sync, hide };
}