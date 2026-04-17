import { createMessageBanner } from './messageBanner.js';

export function createAttractionClosedBanner() {
   return createMessageBanner({
      getMessages: attraction => attraction?.closed_message ? [attraction.closed_message] : [],
   });
}
