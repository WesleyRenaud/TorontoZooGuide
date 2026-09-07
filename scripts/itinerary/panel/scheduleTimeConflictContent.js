import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { ItineraryPanelDom } from './itineraryPanelDom.js';
import { ScheduleTimeConflictContentBuilder } from './scheduleTimeConflictContentBuilder.js';
import { ScheduleConflictCompatibility } from '../wizard/scheduleConflictCompatibility.js';
import { WildEncounterConflictResolution } from '../wizard/wildEncounterConflictResolution.js';

export class ScheduleTimeConflictContent {
   static WILD_ENCOUNTER_TIME_CONFLICT = 'wildEncounterTimeConflict';

   static buildConflictItemImageSrc(item) {
      const file = AssetKeyNormalizer.normalize(item?.name || '');

      if (!file) {
         return null;
      }

      const directory = ScheduleConflictCompatibility.isGuardiansTalkConflictItem(item)
         ? 'guardians-talks'
         : 'wild-encounters';

      return `images/details/${directory}/${file}.png`;

   }

   static createSaveIssuesContent(issues) {
      const content = ItineraryPanelDom.el('div', 'itin-save-issues');
      const wildEncounterConflictIssues = issues.filter(
         issue => issue?.type === ScheduleTimeConflictContent.WILD_ENCOUNTER_TIME_CONFLICT
      );
      let conflictGroups = [];

      if (wildEncounterConflictIssues.length) {
         const sectionResult = ScheduleTimeConflictContentBuilder.createWildEncounterConflictSection(
            WildEncounterConflictResolution.sortWildEncounterConflictIssuesByStartTime(
               wildEncounterConflictIssues
            )
         );

         content.appendChild(sectionResult.section);
         conflictGroups = sectionResult.conflictGroups;
      }

      return {
         content,
         conflictGroups,
      };
   }
}
