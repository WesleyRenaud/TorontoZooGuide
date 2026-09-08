import { AnimalIdentity } from './animalIdentity.js';
import { ItineraryDraftEqualityComparer } from './itineraryDraftEqualityComparer.js';
import { ItineraryDraftModel } from './itineraryDraftModel.js';
import { ItineraryDraftSaveNormalizer } from './itineraryDraftSaveNormalizer.js';
import { ItineraryItemFormatter } from './panel/itineraryItemFormatter.js';
import { TransportationSelectorModel } from './selectors/transportationSelector/transportationSelectorModel.js';

export class ItineraryShape {
   static ITINERARY_ITEM_KEYS = Object.freeze([
      'animals',
      'attractions',
      'guardiansTalks',
      'wildEncounters',
      'transportations',
   ]);

   static normalizeItineraryItems(items) {
      return Array.isArray(items)
         ? items
         : [];
   }

   static createEmptyItineraryDraft() {
      return {
         date: '',
         arrivalTime: '',
         departureTime: '',
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         transportations: [],
         transportationStations: [],
         events: [],
      };
   }

   static normalizeItineraryDraft(draft = {}) {
      const source = ItineraryDraftModel.asItineraryDraftSource(draft);

      return {
         date: ItineraryDraftModel.normalizeItineraryDate(source.date),
         arrivalTime: ItineraryDraftModel.normalizeItineraryTime(source.arrivalTime),
         departureTime: ItineraryDraftModel.normalizeItineraryTime(source.departureTime),
         animals: ItineraryShape.normalizeItineraryItems(source.animals),
         attractions: ItineraryShape.normalizeItineraryItems(source.attractions),
         guardiansTalks: ItineraryShape.normalizeItineraryItems(source.guardiansTalks),
         wildEncounters: ItineraryShape.normalizeItineraryItems(source.wildEncounters),
         transportations: ItineraryShape.normalizeItineraryItems(source.transportations),
         transportationStations: ItineraryShape.normalizeItineraryItems(
            source.transportationStations
         ),
         events: ItineraryShape.normalizeItineraryItems(source.events),
      };
   }

   static cloneItineraryDraft(draft = {}) {
      const normalizedDraft = ItineraryShape.normalizeItineraryDraft(draft);

      return {
         date: normalizedDraft.date,
         arrivalTime: normalizedDraft.arrivalTime,
         departureTime: normalizedDraft.departureTime,
         animals: ItineraryDraftModel.cloneItineraryItems(normalizedDraft.animals),
         attractions: ItineraryDraftModel.cloneItineraryItems(normalizedDraft.attractions),
         guardiansTalks: ItineraryDraftModel.cloneItineraryItems(normalizedDraft.guardiansTalks),
         wildEncounters: ItineraryDraftModel.cloneItineraryItems(normalizedDraft.wildEncounters),
         transportations: ItineraryDraftModel.cloneItineraryItems(normalizedDraft.transportations),
         transportationStations: ItineraryDraftModel.cloneItineraryItems(
            normalizedDraft.transportationStations
         ),
         events: ItineraryDraftModel.cloneItineraryItems(normalizedDraft.events),
      };
   }

   static hydrateWizardDraftFromSavedItinerary(draft = {}) {
      const normalized = ItineraryShape.normalizeItineraryDraft(draft);
      const attractionNames = ItineraryDraftSaveNormalizer.buildAttractionNameSet(normalized.attractions);
      const fromTransportations = normalized.transportations.flatMap((item) => {
         if (!TransportationSelectorModel.isTransportationAddedAsAttraction(item)) {
            return [];
         }

         const name = TransportationSelectorModel.getTransportationName(item);

         if (!name || attractionNames.has(name)) {
            return [];
         }

         attractionNames.add(name);

         return [{ name, addedAsAttraction: true }];
      });

      return {
         ...normalized,
         attractions: [...normalized.attractions, ...fromTransportations],
         transportations: normalized.transportations.filter(
            (item) => !TransportationSelectorModel.isTransportationAddedAsAttraction(item)
         ),
      };
   }

   static toSetItineraryPayload(draft = {}) {
      const base = ItineraryShape.normalizeItineraryDraft(draft);

      return {
         date: base.date,
         arrivalTime: base.arrivalTime,
         departureTime: base.departureTime,
         animals: base.animals.map(AnimalIdentity.normalizeAnimalForSave).filter(Boolean),
         attractions: ItineraryDraftSaveNormalizer.normalizeAttractionsForSave(base.attractions),
         transportations: ItineraryDraftSaveNormalizer.normalizeTransportationsForSave(base),
         guardiansTalks: ItineraryDraftSaveNormalizer.normalizeGuardiansTalkListForSave(base.guardiansTalks),
         wildEncounters: ItineraryItemFormatter.normalizeWildEncounterListForSave(base.wildEncounters),
      };
   }

   static areItineraryDraftsSemanticallyEqual(left, right) {
      const leftSave = ItineraryShape.toSetItineraryPayload(left);
      const rightSave = ItineraryShape.toSetItineraryPayload(right);

      if (leftSave.date !== rightSave.date) {
         return false;
      }

      return ItineraryDraftEqualityComparer.areItineraryDraftSaveItemSelectionsEqual(leftSave, rightSave);
   }

   static areItineraryDraftsEqual(left, right) {
      return ItineraryDraftEqualityComparer.areDraftValuesEqual(
         ItineraryShape.normalizeItineraryDraft(left),
         ItineraryShape.normalizeItineraryDraft(right)
      );
   }

   static isItineraryEmptyDraft(draft = {}) {
      const normalizedDraft = ItineraryShape.normalizeItineraryDraft(draft);

      return !normalizedDraft.date
      && !normalizedDraft.arrivalTime
      && !normalizedDraft.departureTime
      && normalizedDraft.events.length === 0
      && normalizedDraft.transportations.length === 0
      && ItineraryShape.ITINERARY_ITEM_KEYS.every((key) => (
         normalizedDraft[key].length === 0
      ));
   }

   static hasSavedItineraryContent(draft = {}) {
      return !ItineraryShape.isItineraryEmptyDraft(
         ItineraryShape.normalizeItineraryDraft(draft)
      );
   }

   static isItineraryCompletelyUnset(draft = {}) {
      if (!draft || typeof draft !== 'object') {
         return true;
      }

      return ItineraryShape.isItineraryEmptyDraft(
         ItineraryShape.normalizeItineraryDraft(draft)
      );
   }
}
