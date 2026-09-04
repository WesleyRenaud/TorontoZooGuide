import { ItineraryShape } from '../itineraryShape.js';

export class WizardDraft {
   static buildWizardDraft(wizardState, override = {}) {
      return ItineraryShape.normalizeItineraryDraft({
         date: override.date ?? wizardState.date,
         arrivalTime: override.arrivalTime ?? wizardState.arrivalTime,
         departureTime: override.departureTime ?? wizardState.departureTime,
         animals: override.animals ?? wizardState.animals,
         attractions: override.attractions ?? wizardState.attractions,
         guardiansTalks: override.guardiansTalks ?? wizardState.guardiansTalks,
         wildEncounters: override.wildEncounters ?? wizardState.wildEncounters,
         transportations: override.transportations ?? wizardState.transportations,
         transportationStations: override.transportationStations
            ?? wizardState.transportationStations,
         events: override.events ?? wizardState.events,
      });
   }
}
