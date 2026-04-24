import { createSingleMessageBanner } from './messageBanner.js';

export function createAttractionClosedBanner() {
   return createSingleMessageBanner(
      attraction => attraction?.closed_message
   );
}
