import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';

function getGenericDescription() {
   return `Join our knowledgeable Guardians as they share fascinating facts about our animal residents. Discover how they
      are cared for, learn about conservation efforts, and explore the important role enrichment plays in their
      well-being. You may also see the animals enjoying their meals, learn about their diets, and observe their natural
      behaviours in action. Follow the schedule below to learn more about your favourite Toronto Zoo animals!`;
}

export const guardiansTalkRenderer = {
   key: 'guardiansTalk',

   createCard(t, index) {
      const name = t.name || 'Meet The Guardians Talk';
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/guardians-talks/${normalizedName}.png`,
            alt: t.name || name,
            fallbackSrc: 'images/icons/guardians-talk/guardians-talk.png',
         },
         title: { text: name },
         details: [
            `Location: ${t.location}`,
            `Start Time: ${t.time_of_day}`,
            `Description: ${getGenericDescription()}`,
         ],
      });
   },
};
