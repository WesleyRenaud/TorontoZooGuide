import { MessageFragment } from './messageFragment.js';

export class AttractionClosedFragment {
   static createAttractionClosedBanner() {
      return MessageFragment.createSingleMessageBanner(
         attraction => attraction?.closed_message
      );
   }
}
