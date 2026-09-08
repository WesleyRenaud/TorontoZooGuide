export class PastItineraryPromptTracker {
   static pastItineraryPromptOpen = false;

   static isPastItineraryPromptOpen() {
      return PastItineraryPromptTracker.pastItineraryPromptOpen;
   }

   static setPastItineraryPromptOpen(isOpen) {
      PastItineraryPromptTracker.pastItineraryPromptOpen = isOpen;
   }

   static resetPastItineraryPromptSessionForTests() {
      PastItineraryPromptTracker.pastItineraryPromptOpen = false;
   }
}
