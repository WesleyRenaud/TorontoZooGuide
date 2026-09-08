export class PromptSession {
   static pastItineraryPromptOpen = false;

   static isPastItineraryPromptOpen() {
      return PromptSession.pastItineraryPromptOpen;
   }

   static setPastItineraryPromptOpen(isOpen) {
      PromptSession.pastItineraryPromptOpen = isOpen;
   }

   static resetPastItineraryPromptSessionForTests() {
      PromptSession.pastItineraryPromptOpen = false;
   }
}
