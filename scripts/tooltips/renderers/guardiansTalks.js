import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';

export const guardiansTalkRenderer = {
   key: 'guardiansTalk',

   getGenericDescription() {
      return   `Join our knowledgeable Guardians as they share fascinating facts about our animal residents. Discover how they
               are cared for, learn about conservation efforts, and explore the important role enrichment plays in their
               well-being. You may also see the animals enjoying their meals, learn about their diets, and observe their natural
               behaviours in action. Follow the schedule below to learn more about your favourite Toronto Zoo animals!`;
   },

   createCard(t, index) {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = index;
      card.style.display = index === 0 ? 'flex' : 'none';

      const name = t.name || 'Meet The Guardians Talk';
      const normalizedName = normalizeAssetKey(name);

      card.innerHTML = `
         <div class="tooltip-image-frame">
         <img
            src="images/guardians-talks/${normalizedName}.png"
            alt="${t.name}"
            class="tooltip-image"
         >
         </div>

         <strong>${name}</strong>
         <span>Location: ${t.location}</span>
         <span>Start Time: ${t.time_of_day}</span>
         <span>Description: ${this.getGenericDescription()}</span>
      `;
      return card;
   },
};
