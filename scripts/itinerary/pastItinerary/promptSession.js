let pastItineraryPromptOpen = false;

export function isPastItineraryPromptOpen() {
   return pastItineraryPromptOpen;
}

export function setPastItineraryPromptOpen(isOpen) {
   pastItineraryPromptOpen = isOpen;
}

export function resetPastItineraryPromptSessionForTests() {
   pastItineraryPromptOpen = false;
}
