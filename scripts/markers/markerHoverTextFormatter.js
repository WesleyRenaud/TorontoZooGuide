import { Strings } from '../strings.js';

export class MarkerHoverTextFormatter {
   static readItemText(item, field, fallback) {
      return item?.[field] || fallback;
   }

   static formatCountedHoverText(itemsAtPoint, getTitle) {
      const firstTitle = getTitle(itemsAtPoint[0]);

      if (itemsAtPoint.length === 1) {
         return firstTitle;
      }

      return `${firstTitle} + ${itemsAtPoint.length - 1}`;
   }

   static formatGuardiansTalkHoverText(itemsAtPoint) {
      return MarkerHoverTextFormatter.formatCountedHoverText(itemsAtPoint, (item) => {
         const name = item?.name || '';
         return name
            ? Strings.map.hover.guardiansTalkWithName(name)
            : Strings.entityLabels.guardiansTalk;
      });
   }

   static formatWildEncounterHoverText(itemsAtPoint) {
      if (itemsAtPoint.length === 1) {
         const name = itemsAtPoint[0]?.name || '';
         return name
            ? Strings.map.hover.wildEncounterMeetingSpotWithName(name)
            : Strings.map.hover.wildEncounterMeetingSpot;
      }

      const first = itemsAtPoint[0]?.name || Strings.map.hover.wildEncounterMeetingSpot;
      return Strings.map.hover.wildEncounterMultiple(first, itemsAtPoint.length - 1);
   }
}
