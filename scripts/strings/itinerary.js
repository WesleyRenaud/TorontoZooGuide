export const itinerary = {
   actions: {
      accept: 'Accept',
      add: 'Add',
      addSymbol: '+',
      build: 'Build Itinerary',
      cancel: 'Cancel',
      clear: 'Clear',
      edit: 'Edit',
      editItinerary: 'Edit Itinerary',
      finish: 'Finish',
      next: 'Next',
      previous: 'Previous',
      remove: '−',
      discard: 'Discard',
   },
   aria: {
      addToItinerary: 'Add to itinerary',
      addToItineraryWithScheduleOverride: (
         'Add to itinerary with adjusted talk time'
      ),
      closeBuilder: 'Close itinerary builder',
      panel: 'Itinerary panel',
      removeFromItinerary: 'Remove from itinerary',
      removeFromItineraryWithScheduleOverride: (
         'Remove from itinerary with adjusted talk time'
      ),
      selectRegionsAndExhibits: 'Select regions and exhibits',
   },
   confirmation: {
      attractionMayBeClosed: 'Attraction May Be Closed',
      clearMessage: (
         'This will remove all selected Animals, Attractions, Meet the Guardians talks, and Wild Encounters.'
      ),
      clearTitle: 'Clear Itinerary?',
      saveChangesMessage: (
         'You have unsaved itinerary changes. Would you like to save them before closing?'
      ),
      saveChangesTitle: 'Save Changes?',
      saveIssuesButton: 'Proceed',
      proceedAnyway: 'Proceed Anyway',
      saveIssuesTitle: 'Your Itinerary Has the Following Issues:',
      proceedWithoutConflictSelectionMessage: (
         'None of these conflicting activities will be added to your itinerary.'
      ),
      proceedWithoutConflictSelectionTitle: (
         'Proceed Without Selecting an Activity?'
      ),
      proceedWithUnresolvedConflictsMessage: (
         'You have not made a selection for every conflict. Only the activities you selected will be added to your itinerary.'
      ),
      proceedWithUnresolvedConflictsTitle: (
         'Proceed Without Resolving All Conflicts?'
      ),
      proceedWithAdditionalSelectableActivitiesMessage: (
         'You can still add more conflicting activities that do not overlap with your current selections.'
      ),
      proceedWithAdditionalSelectableActivitiesTitle: (
         'Add More Activities?'
      ),
      closeSaveIssuesTitle: 'Close Without Adding an Activity?',
      scheduleConflictsMessage: (
         'Select the activities you want. You can add more than one as long as their times do not overlap.'
      ),
      scheduleConflictsTitle: 'Schedule Conflicts',
      scheduleOverrideSelectionMessage: (
         'These selections overlap in time. We’ll fit them into your day by shortening some activities, with Wild Encounters taking priority.'
      ),
      scheduleOverrideSelectionTitle: 'Adjust Activity Times?',
      shortVisitTitle: 'Short Visit?',
      shortVisitMessage: (
         'Your arrival and departure times are very close together. '
         + 'Are you sure you want to save these times?'
      ),
      doNotShowAgain: 'Don’t show this again',
      scheduleItemNotOnItineraryTitle: 'Add to Itinerary?',
      scheduleItemNotOnItineraryMessage: (
         'This item is not on your itinerary yet. '
         + 'Do you want to add it and schedule a time?'
      ),
      scheduleItemNotOnItineraryConfirm: 'Add to Schedule',
      guardiansTalkUnscheduleTitle: 'Unschedule Conflicting Items?',
      guardiansTalkUnscheduleMessage: talksList => `Adding these Meet the Guardians Talks: ${talksList} will unschedule other items that overlap their time. Do you want to continue?`,
      guardiansTalkUnscheduleConfirm: 'Continue',
      wildEncounterUnscheduleMessage: encountersList => `Adding these Wild Encounters: ${encountersList} will unschedule other items that overlap their time. Do you want to continue?`,
      removeItemTitle: 'Remove from Itinerary?',
      removeItemMessage: (
         'It will no longer appear in your day plan or itinerary lists. You can add it again later from the itinerary builder.'
      ),
      animalMayBeOffDisplay: 'Animal May Be Off Display',
   },
   emptyText: {
      animals: 'No animals found.',
      attractions: 'No attractions found.',
      guardiansTalks: 'No Meet the Guardians talks found for this day',
      regions: 'No regions available right now.',
      results: 'No results found.',
      wildEncounters: 'No wild encounters found for this day',
   },
   emptyPanel: 'Build an itinerary to see it here.',
   errors: {
      generic: 'Could not update itinerary.',
      arrivalDepartureTooClose: 'Could not update itinerary time.',
      noAvailableSlot: 'No open time slot is available for this item.',
      requestedTimeNotAvailable: (
         'That time is not available. Select another start time and try again.'
      ),
      itemNotOnItinerary: 'This item must be on your itinerary before it can be scheduled.',
   },
   dayPlanner: {
      aria: 'Itinerary day planner preview',
      arrivalInputLabel: 'Arrival time',
      clearArrivalTimeAria: 'Clear arrival time',
      arrivalTimeInvalid: (
         'Arrival time must be between opening and last admission.'
      ),
      arrivalTimeBeforeDepartureInvalid: (
         'Arrival time must be before departure.'
      ),
      arrivalLabel: 'Arrival',
      arrivalTimeMenuAria: 'Arrival time options',
      remove: 'Remove',
      unschedule: 'Unschedule',
      scheduledItemMenuAria: 'Scheduled item options',
      dayPlannerLabel: 'Day Planner View',
      date: 'Saturday, June 20',
      departureInputLabel: 'Departure time',
      clearDepartureTimeAria: 'Clear departure time',
      departureTimeMenuAria: 'Departure time options',
      departureTimeInvalid: (
         'Departure time must be between opening and closing.'
      ),
      departureTimeAfterArrivalInvalid: (
         'Departure time must be after arrival.'
      ),
      earlyAdmissionLabel: 'Early Admission',
      firstSlot: '9:30 AM',
      listViewLabel: 'List View',
      closeLabel: 'Zoo Closes',
      hoursUnavailable: 'Zoo hours are unavailable for this date.',
      lastAdmissionLabel: 'Last Admission',
      openLabel: 'Zoo Opens',
      secondSlot: '10:00 AM',
      thirdSlot: '10:30 AM',
      title: 'Day Plan',
      scheduledTitle: 'Scheduled Items',
      unscheduledTitle: 'Unscheduled Items',
      scheduleItemButton: 'Schedule an item',
   },
   scheduleItem: {
      title: 'Schedule item',
      errorTitle: 'Unable to Schedule',
      scheduleButton: 'Schedule',
      typeLabel: 'Item type',
      typePlaceholder: 'Choose what to schedule',
      searchLabel: 'Search',
      searchPlaceholder: 'Search your itinerary items',
      onlyItineraryItemsLabel: 'Only show items on my itinerary',
      timeLabel: 'Schedule time',
      timePlaceholder: '--:-- --',
      durationLabel: 'Duration',
      durationPlaceholder: 'Minutes (optional)',
      durationRequiresTime: 'Enter a time before setting a duration.',
      emptyResults: 'No matching items found.',
      selectItem: 'Select item',
      itemSelected: 'Selected',
   },
   itemImage: title => `${title} image`,
   itemPhoto: title => `${title} photo`,
   noItemsSelected: {
      button: 'OK',
      message: (
         'Please add at least one Animal, Attraction, Meet the Guardians talk, or Wild Encounter before finishing.'
      ),
      title: 'No Items Selected',
   },
   removedItems: {
      animalsAddedSubtitle: (
         'The following animals from your selected exhibits are available on your new date and were added to your itinerary.'
      ),
      animalsAddedTitle: 'Animals Added',
      animalsRemovedSubtitle: (
         'The following animals are unavailable on your new date for the reasons listed below.'
      ),
      animalsRemovedTitle: 'Animals Removed',
      attractionsSubtitle: 'The following attractions are unavailable on your new date.',
      // TO-DO: This string should be updated. It is not that the animals are easier to see, but rather that are more
      // likely to be on display.
      improvedAnimalVisibilitySubtitle: (
         'The following animals remain on your itinerary and are expected to be easier to see on your new date.'
      ),
      improvedAnimalVisibilityTitle: 'Improved Animal Visibility',
      itineraryUpdated: 'Itinerary Updated',
      emptyItinerarySubtitle: (
         'None of your selected items are available on the new date. You can view alternatives below.'
      ),
      reducedAnimalVisibilitySubtitle: (
         'The following animals remain on your itinerary, but are expected to be less visible on your new date.'
      ),
      reducedAnimalVisibilityTitle: 'Reduced Animal Visibility',
      someDetailsChanged: 'Some itinerary details changed',
      talksSubtitle: 'The following talks are not scheduled on your new date.',
      changedSubtitle: 'Some itinerary items changed for your new date. Review the updates below.',
      viewAlternatives: 'View Alternatives',
      wildEncountersSubtitle: 'The following encounters are not available on your new date.',
      emptyItineraryTitle: 'Your itinerary is now empty',
      keepInItinerary: 'Keep',
      removeFromItineraryHint: 'This item will stay on your itinerary when you accept.',
   },
   searchPlaceholder: 'Search...',
   selectors: {
      animalSubtitle: 'Search and add animals to your plan.',
      attractionSubtitle: 'Search and add attractions to your plan.',
      builderTitle: 'Itinerary Builder',
      guardiansTalkSubtitle: 'Search and add talks to your plan.',
      includeOffDisplayAnimals: 'Include off-display animals',
      lowVisibilityHint: 'Very low chance of seeing this animal',
      titleAnimals: 'Add Animals',
      titleAttractions: 'Add Attractions',
      titleDate: 'Set Visit Date',
      titleRegions: 'Add Animals by Region',
      talkFallback: 'Talk',
      meetingSpot: 'Meeting Spot',
      visitDate: 'Visit Date',
      visitDateSubtitle: 'Choose the date for your visit.',
      wildEncounterSubtitle: 'Search and add wild encounters to your plan.',
   },
};
