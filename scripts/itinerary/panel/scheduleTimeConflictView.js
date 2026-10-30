import { ItineraryPanelHelper } from './itineraryPanelHelper.js';
import { RowPresenter } from './rowPresenter.js';
import { ScheduleTimeConflictContentBuilder } from './scheduleTimeConflictContentBuilder.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { WildEncounterConflictResolver } from '../wizard/wildEncounterConflictResolver.js';

export class ScheduleTimeConflictView {
   static buildGuardiansTalkConflictImageSrc(item) {
      return RowPresenter.buildImageSrc('guardians-talks', item.location, item.name);
   }

   static buildWildEncounterConflictImageSrc(item) {
      return RowPresenter.buildImageSrc('wild-encounters', item.name);
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
