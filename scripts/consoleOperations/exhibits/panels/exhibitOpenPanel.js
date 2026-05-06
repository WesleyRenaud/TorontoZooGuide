import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createExhibitOpenPanel() {
   return createPanelShell({
      panelId: 'exhibitOpenPanel',
      title: APP_STRINGS.panelTitles.exhibitOpen,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.exhibit,
            inputId: 'exhibitOpenExhibit',
            emptyOptionLabel: APP_STRINGS.placeholders.exhibit,
         }),
         createDateRangeFields({
            startDateId: 'exhibitOpenStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'exhibitOpenEndDate',
            endHelpText: APP_STRINGS.help.keepExplicitlyOpenUntilChanged('exhibit'),
         }),
         createActions({
            submitId: 'submitExhibitOpen',
         }),
         createStatus({
            statusId: 'exhibitOpenStatus',
         }),
      ],
   });
}
