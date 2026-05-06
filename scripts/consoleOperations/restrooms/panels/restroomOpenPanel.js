import {
   createActions,
   createDateRangeFields,
   createPanelShell,
   createSelectField,
   createStatus,
} from '../../templates/fragments.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRestroomOpenPanel() {
   return createPanelShell({
      panelId: 'restroomOpenPanel',
      title: APP_STRINGS.panelTitles.restroomOpen,
      bodyChildren: [
         createSelectField({
            label: APP_STRINGS.entityLabels.restroom,
            inputId: 'restroomOpenRestroom',
            emptyOptionLabel: APP_STRINGS.placeholders.restroom,
         }),
         createDateRangeFields({
            startDateId: 'restroomOpenStartDate',
            startHelpText: APP_STRINGS.help.startImmediately,
            endDateId: 'restroomOpenEndDate',
            endHelpText: APP_STRINGS.help.keepExplicitlyOpenUntilChanged('restroom'),
         }),
         createActions({
            submitId: 'submitRestroomOpen',
         }),
         createStatus({
            statusId: 'restroomOpenStatus',
         }),
      ],
   });
}
