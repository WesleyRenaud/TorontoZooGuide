let pastItineraryPromptOpen = false;

export class PromptSession {
   static isPastItineraryPromptOpen() {
      return pastItineraryPromptOpen;
   }

   static setPastItineraryPromptOpen(isOpen) {
      pastItineraryPromptOpen = isOpen;
   }

   static resetPastItineraryPromptSessionForTests() {
      pastItineraryPromptOpen = false;
   }
}
