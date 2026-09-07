import { ValueNormalizer } from '../api/valueNormalizer.js';
import { ItineraryShape } from './itineraryShape.js';
import { ItineraryItemFormatter } from './panel/itineraryItemFormatter.js';
import { TransportationSelectorModel } from './selectors/transportationSelector/transportationSelectorModel.js';

export class ItineraryDraftSaveNormalizer {
   static normalizeGuardiansTalkListForSave(items) {
      return ItineraryShape.normalizeItineraryItems(items)
         .map(ItineraryItemFormatter.normalizeGuardiansTalkForSave)
         .filter((talk) => talk.name);
   }

   static normalizeTransportationNameForSave(item) {
      if (typeof item === 'string') {
         return ValueNormalizer.asTrimmedString(item);
      }

      if (!item || typeof item !== 'object') {
         return '';
      }

      return ValueNormalizer.asTrimmedString(item.name);
   }

   static getAttractionDraftName(item) {
      if (typeof item === 'string') {
         return ValueNormalizer.asTrimmedString(item);
      }

      return ValueNormalizer.asTrimmedString(item?.name);
   }

   static buildAttractionNameSet(attractions = []) {
      return new Set(
         ItineraryShape.normalizeItineraryItems(attractions)
            .map(ItineraryDraftSaveNormalizer.getAttractionDraftName)
            .filter(Boolean)
      );
   }

   static isAttractionAddedAsAttraction(item) {
      return Boolean(item && typeof item === 'object' && item.addedAsAttraction === true);
   }

   static normalizeTransportationsForSave(draft = {}) {
      const fromAttractions = ItineraryShape.normalizeItineraryItems(draft.attractions)
         .filter(ItineraryDraftSaveNormalizer.isAttractionAddedAsAttraction)
         .map((item) => ({
            name: ItineraryDraftSaveNormalizer.normalizeTransportationNameForSave(item),
            added_as_attraction: true,
         }))
         .filter((item) => item.name);

      const fromTransportations = ItineraryShape.normalizeItineraryItems(draft.transportations)
         .map((item) => {
            const name = ItineraryDraftSaveNormalizer.normalizeTransportationNameForSave(item);

            if (!name) {
               return null;
            }

            return {
               name,
               added_as_attraction: (
                  TransportationSelectorModel.isTransportationAddedAsAttraction(item)
                  || ItineraryDraftSaveNormalizer.isAttractionAddedAsAttraction(item)
               ),
            };
         })
         .filter(Boolean);

      const bySaveKey = new Map();

      [...fromTransportations, ...fromAttractions].forEach((item) => {
         bySaveKey.set(
            `${item.name}::${item.added_as_attraction}`,
            item
         );
      });

      return [...bySaveKey.values()];
   }

   static normalizeAttractionsForSave(attractions = []) {
      return ItineraryItemFormatter.normalizeItineraryNamesForSave(
         ItineraryShape.normalizeItineraryItems(attractions).filter((item) => (
            !ItineraryDraftSaveNormalizer.isAttractionAddedAsAttraction(item)
         ))
      );
   }
}
