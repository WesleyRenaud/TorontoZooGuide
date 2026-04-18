import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';

export const zoomobileStationRenderer = {
   key: 'zoomobileStation',

   createCard(s, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const name = s.name || 'Zoomobile Station';
      const normalizedName = normalizeAssetKey(name);
      const imgSrc = `images/zoomobile-stations/${normalizedName}.png`;

      card.innerHTML = `
         <div class="tooltip-image-frame">
         <img
            src="${imgSrc}"
            alt="${name}"
            class="tooltip-image"
            onerror="this.onerror=null; this.src='images/generic-icons/zoomobile-station.png';"
         >
         </div>

         <strong>${name}</strong>
         ${s.description ? `<span>Description: ${s.description}</span>` : ''}       
      `;
      return card;
   },
};
