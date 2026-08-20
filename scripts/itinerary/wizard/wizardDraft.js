import { normalizeItineraryDraft } from '../itineraryShape.js';

export function buildWizardDraft(wizardState, override = {}) {
   return normalizeItineraryDraft({
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
