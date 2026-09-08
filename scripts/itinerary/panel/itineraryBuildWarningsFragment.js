import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { ItineraryBuildWarningsContentBuilder } from './itineraryBuildWarningsContentBuilder.js';
import { Strings } from '../../strings.js';

export class ItineraryBuildWarningsFragment {
   static getItineraryBuildWarningTypes(issues = []) {
      const warningTypes = ItineraryBuildWarningsContentBuilder.itineraryBuildWarningIssueTypes();
      const presentTypes = new Set(
         issues
            .map(ItineraryBuildWarningsContentBuilder.issueType)
            .filter((type) => warningTypes.includes(type))
      );

      return warningTypes.filter((type) => presentTypes.has(type));

   }

   static buildConfirmedOptionsFromBuildWarnings(issues = []) {
      const confirmFlags = ItineraryBuildWarningsContentBuilder.buildWarningConfirmFlags();

      return ItineraryBuildWarningsFragment.getItineraryBuildWarningTypes(issues).reduce(
         (flags, type) => ({
            ...flags,
            ...confirmFlags[type],
         }),
         {}
      );

   }

   static buildItineraryBuildWarningSections(issues = []) {
      return ItineraryBuildWarningsContentBuilder.BUILD_WARNING_SECTION_LIST_BUILDERS.flatMap(
         (buildSections) => buildSections(issues, Strings.itinerary.confirmation)
      );
   }

   static hasMultipleItineraryBuildWarnings(issues = []) {
      return ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections(issues).length > 1;

   }

   static showItineraryBuildWarningsConfirmation({
      issues = [],
      onConfirm,
      onCancel,
      mountEl = ItineraryPanelFragment.getItineraryOverlayMountEl() ?? document.body,
   } = {}) {
      const sections = ItineraryBuildWarningsFragment.buildItineraryBuildWarningSections(issues);

      if (sections.length === 0) {
         onCancel?.();
         return;
      }

      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.saveIssuesTitle,
         bodyContent: ItineraryBuildWarningsContentBuilder.createBuildWarningsContent(sections),
         confirmText: Strings.itinerary.confirmation.saveIssuesButton,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl,
         onConfirm,
         onCancel,
      });
   }
}
