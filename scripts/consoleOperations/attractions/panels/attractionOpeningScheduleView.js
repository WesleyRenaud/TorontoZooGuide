import { AmenityOpeningSchedulePanelBuilder } from '../../forms/amenityOpeningSchedulePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class AttractionOpeningScheduleView {
   static createAttractionOpeningSchedulePanel() {
      return AmenityOpeningSchedulePanelBuilder.createPanel({
         panelId: 'attractionOpeningSchedulePanel',
         title: Strings.panelTitles.attractionOpeningSchedule,
         entityLabel: Strings.entityLabels.attraction,
         emptyOptionLabel: Strings.placeholders.attraction,
         idPrefix: 'attractionOpeningSchedule',
         entityFieldName: 'Attraction',
         scheduleMessagePlaceholder: Strings.textareas.scheduledClosedMessage('attraction'),
         submitId: 'submitAttractionOpeningSchedule',
         statusId: 'attractionOpeningScheduleStatus',
      });
   }
}
