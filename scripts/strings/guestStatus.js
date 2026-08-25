/** Guest-facing API copy. Templates use {param} placeholders (Python str.format compatible). */
export const guestStatus = {
   animals: {
      temporarilyOffDisplay: 'The {species} is temporarily off-display.',
      viewingAlert: 'The {species} may be less visible than usual at this time.',
      singleHabitatAlternateEnclosureViewingAlert: (
         'If you do not see the {species} {chosenLocation}, '
         + 'then check their {alternateHabitat} habitat.'
      ),
      limitedViewingSchedule: (
         'The {species} is viewable daily only from '
         + '{dailyStartTime} to {dailyEndTime}.'
      ),
      limitedViewingScheduleUntil: (
         'The {species} is viewable daily only from '
         + '{dailyStartTime} to {dailyEndTime}until {endDate}.'
      ),
      exhibitLikelyClosedOnDay: (
         'The {exhibit} is most likely closed on this day.'
      ),
      speciesLikelyOffDisplayOnDay: (
         'The {species} is most likely off display on this day.'
      ),
   },
   attractions: {
      weekendsAndHolidaysOnly: (
         'The {attractionName} is open on weekends and holidays only.'
      ),
      notScheduledToday: (
         'The {attractionName} is not scheduled to be open today.'
      ),
      likelyNotOperating: (
         'The {attractionName} is most likely not operating on this day.'
      ),
   },
   locations: {
      temporarilyClosed: 'The {name} is temporarily closed.',
      notScheduledToBeOpenToday: (
         'The {name} is not scheduled to be open today.'
      ),
      likelyNotOpenOnDay: 'The {name} is most likely not open on this day.',
   },
   drinkingFountains: {
      closedForSeason: 'The drinking fountains are closed for the season.',
   },
   wildEncounters: {
      notScheduledToday: 'The {wildEncounter} is not scheduled today.',
   },
   guardiansTalks: {
      notScheduledToday: (
         'The {talkName} at {location} is not scheduled today.'
      ),
   },
   itinerary: {
      guardiansTalkFullyCoveredByBlocker: (
         'Guardians talk interval is fully covered by a scheduled blocker.'
      ),
      guardiansTalkUnexpectedBlockerOverlap: (
         'Guardians talk interval overlaps a blocker in an unexpected way.'
      ),
      guardiansTalkNoRemainingTimeAfterTrimming: (
         'Guardians talk has no remaining time after trimming.'
      ),
      wildEncounterRowMissingStartTime: (
         'Wild encounter row {wildEncounter} is missing a start time.'
      ),
   },
   visitDaySchedule: {
      notScheduledOnVisitDay: '{name} is not scheduled on {month} {day}.',
      notOfferedThisWeekday: '{name} is not offered on this day of the week.',
      cancelledForThisDate: '{name} has been cancelled for this date.',
   },
};
