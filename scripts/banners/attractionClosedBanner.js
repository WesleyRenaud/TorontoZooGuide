import { MessageBanner } from './messageBanner.js';

export class AttractionClosedBanner {
   static createAttractionClosedBanner() {
      return MessageBanner.createSingleMessageBanner(
         attraction => attraction?.closed_message
      );
   }
}
