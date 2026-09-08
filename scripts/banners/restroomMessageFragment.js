import { MessageFragment } from './messageFragment.js';

export class RestroomMessageFragment {
   static createRestroomMessageBanner() {
      return MessageFragment.createSingleMessageBanner(
         restroom => restroom?.closed_message || restroom?.alert_message
      );
   }
}
