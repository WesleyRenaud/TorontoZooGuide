import { AssetKeyNormalizer } from '../../../assets/assetKeyNormalizer.js';
import { StoredSelection } from '../base/storedSelection.js';
import { ScheduledOccurrencePresentation } from '../../scheduledOccurrencePresentation.js';
import { ScheduledOccurrenceTimeRange } from '../../scheduledOccurrenceTimeRange.js';
import { Strings } from '../../../strings.js';

const DEFAULT_ATTRACTION_TITLE = 'Attraction';
const CLOSED_ATTRACTION_FALLBACK_NAME = 'This attraction';

function createStoredAttractionFromString(item) {
   const name = StoredSelection.normalizeStoredString(item);

   if (!name) {
      return null;
   }

   return {
      id: name,
      name,
      subtitle: '',
      freeWithAdmission: false,
      seasonal: false,
      isClosed: false,
      addedAsAttraction: false,
      infoLink: null,
      imageSrc: null,
   };
}

function createStoredAttractionFromObject(item) {
   const name = StoredSelection.normalizeStoredString(item.name);
   const id = StoredSelection.normalizeStoredId(item.id, name);

   if (!id) {
      return null;
   }

   return {
      id,
      name,
      subtitle: StoredSelection.normalizeStoredString(item.subtitle),
      freeWithAdmission: StoredSelection.normalizeStoredBoolean(item.freeWithAdmission),
      seasonal: StoredSelection.normalizeStoredBoolean(item.seasonal),
      isClosed: StoredSelection.normalizeStoredBoolean(item.isClosed),
      addedAsAttraction: StoredSelection.normalizeStoredBoolean(item.addedAsAttraction),
      infoLink: StoredSelection.normalizeStoredLink(item.infoLink),
      imageSrc: StoredSelection.normalizeStoredLink(item.imageSrc),
   };
}

export class AttractionSelectorModel {
   static getAttractionName(row) {
      return typeof row?.name === 'string'
         ? row.name
         : '';
   }

   static getAttractionId(row) {
      return AttractionSelectorModel.getAttractionName(row);
   }

   static getAttractionTitle(row) {
      return AttractionSelectorModel.getAttractionName(row) || DEFAULT_ATTRACTION_TITLE;
   }

   static getAttractionInfoLink(row) {
      const value = row?.info_link ?? null;
      const link = typeof value === 'string' ? value.trim() : '';
      return link || null;
   }

   static isFreeWithAdmission(row) {
      return row?.free_with_admission === true;
   }

   static isSeasonalAttraction(row) {
      return row?.part_of_seasonal_attraction === true;
   }

   static isClosedAttraction(row) {
      return row?.is_closed === true;
   }

   static isAlsoTransportationAttraction(row) {
      return row?.is_also_transportation === true;
   }

   static getAttractionSubtitle(row) {
      return ScheduledOccurrencePresentation.buildOccurrenceSubtitle({
         primaryValue: AttractionSelectorModel.isFreeWithAdmission(row)
            ? Strings.search.freeWithAdmission
            : Strings.search.extraCharge,
         timeRange: ScheduledOccurrenceTimeRange.buildScheduledOccurrenceTimeRange({
            start_time: row?.open_time,
            end_time: row?.close_time,
         }),
      });
   }

   static buildAttractionImageSrc(row) {
      const attractionFile = AssetKeyNormalizer.normalize(
         AttractionSelectorModel.getAttractionName(row)
      );

      if (!attractionFile) {
         return null;
      }

      return `../images/details/attractions/${attractionFile}.png`;
   }

   static migrateStoredAttractions(items) {
      return StoredSelection.migrateStoredSelectionItems(items, {
         fromString: createStoredAttractionFromString,
         fromObject: createStoredAttractionFromObject,
      });
   }

   static makeAttractionSelection(row) {
      return {
         id: AttractionSelectorModel.getAttractionId(row),
         name: AttractionSelectorModel.getAttractionName(row),
         subtitle: AttractionSelectorModel.getAttractionSubtitle(row),
         freeWithAdmission: AttractionSelectorModel.isFreeWithAdmission(row),
         seasonal: AttractionSelectorModel.isSeasonalAttraction(row),
         isClosed: AttractionSelectorModel.isClosedAttraction(row),
         addedAsAttraction: AttractionSelectorModel.isAlsoTransportationAttraction(row),
         infoLink: AttractionSelectorModel.getAttractionInfoLink(row),
         imageSrc: AttractionSelectorModel.buildAttractionImageSrc(row),
      };
   }

   static shouldConfirmClosedAttraction({
      row,
      isSelected,
      includeClosedAttractions,
   } = {}) {
      if (isSelected) {
         return false;
      }

      if (!includeClosedAttractions) {
         return false;
      }

      return AttractionSelectorModel.isClosedAttraction(row);
   }

   static shouldConfirmAlsoTransportationAttraction({
      row,
      isSelected,
   } = {}) {
      if (isSelected) {
         return false;
      }

      return AttractionSelectorModel.isAlsoTransportationAttraction(row);
   }

   static buildClosedAttractionMessage(row) {
      const name = AttractionSelectorModel.getAttractionName(row)
         || CLOSED_ATTRACTION_FALLBACK_NAME;
      return `The ${name} is closed on your visit date. Do you still want to add it to your itinerary?`;
   }

   static buildAlsoTransportationAttractionMessage(row) {
      return Strings.itinerary.confirmation.attractionAlsoTransportationMessage(
         AttractionSelectorModel.getAttractionName(row)
      );
   }
}
