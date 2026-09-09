import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { ItineraryPanelHelper } from './itineraryPanelHelper.js';
import { ScheduleTimeConflictContentBuilder } from './scheduleTimeConflictContentBuilder.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { ScheduleConflictChecker } from '../wizard/scheduleConflictChecker.js';
import { WildEncounterConflictResolver } from '../wizard/wildEncounterConflictResolver.js';

export class ScheduleTimeConflictView {
   static buildConflictItemImageSrc(item) {
      const file = AssetKeyNormalizer.normalize(item?.name || '');

      if (!file) {
         return null;
      }

      const directory = ScheduleConflictChecker.isGuardiansTalkConflictItem(item)
         ? 'guardians-talks'
         : 'wild-encounters';

      return `images/details/${directory}/${file}.png`;

   }

   static createSaveIssuesContent(issues) {
      const content = ItineraryPanelHelper.el('div', 'itin-save-issues');
      const wildEncounterConflictIssues = issues.filter(
         issue => issue?.type === ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT
      );
      let conflictGroups = [];

      if (wildEncounterConflictIssues.length) {
         const sectionResult = ScheduleTimeConflictContentBuilder.createWildEncounterConflictSection(
            WildEncounterConflictResolver.sortWildEncounterConflictIssuesByStartTime(
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
