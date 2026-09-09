import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { AssetKeyNormalizer } from '../../../assets/assetKeyNormalizer.js';
import { AttractionSelectorStoredAttractionFactory } from './attractionSelectorStoredAttractionFactory.js';
import { StoredSelectionNormalizer } from '../base/storedSelectionNormalizer.js';
import { ScheduledOccurrencePresenter } from '../../scheduledOccurrencePresenter.js';
import { ScheduledOccurrenceTimeModel } from '../../scheduledOccurrenceTimeModel.js';
import { Strings } from '../../../strings.js';

export class AttractionSelectorModel {
   static DEFAULT_ATTRACTION_TITLE = 'Attraction';

   static CLOSED_ATTRACTION_FALLBACK_NAME = Strings.itinerary.confirmation.closedAttractionFallbackName;

   static getAttractionName(row) {
      return typeof row?.name === 'string'
         ? row.name
         : '';
   }

   static getAttractionId(row) {
      return AttractionSelectorModel.getAttractionName(row);
   }

   static getAttractionTitle(row) {
      return AttractionSelectorModel.getAttractionName(row) || AttractionSelectorModel.DEFAULT_ATTRACTION_TITLE;
   }

   static getAttractionInfoLink(row) {
      const value = row?.info_link ?? null;
      const link = ValueNormalizer.asTrimmedString(value);
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
      return ScheduledOccurrencePresenter.buildOccurrenceSubtitle({
         primaryValue: AttractionSelectorModel.isFreeWithAdmission(row)
            ? Strings.search.freeWithAdmission
            : Strings.search.extraCharge,
         timeRange: ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange({
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
      return StoredSelectionNormalizer.migrateStoredSelectionItems(items, {
         fromString: AttractionSelectorStoredAttractionFactory.createStoredAttractionFromString,
         fromObject: AttractionSelectorStoredAttractionFactory.createStoredAttractionFromObject,
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
         || AttractionSelectorModel.CLOSED_ATTRACTION_FALLBACK_NAME;
      return Strings.itinerary.confirmation.closedAttractionMessage(name);
   }

   static buildAlsoTransportationAttractionMessage(row) {
      return Strings.itinerary.confirmation.attractionAlsoTransportationMessage(
         AttractionSelectorModel.getAttractionName(row)
      );
   }
}
