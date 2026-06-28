import { ScheduleItemKind } from '../../../scripts/shared/enums/scheduleItemKind.js';

export function makeScheduledItem(
      label,
      startMinutes,
      maximumDuration = 30,
      anchorSlotMinutes = 570,
      viewingWalkNodeId = '' ) {
   return {
      label,
      startMinutes,
      endMinutes: startMinutes + maximumDuration,
      maximumDuration,
      offsetFraction: (startMinutes - anchorSlotMinutes) / 30,
      anchorSlotMinutes,
      item: {
         species: label,
         start_time: '10:00 AM',
         end_time: '10:30 AM',
         viewing_walk_node_id: viewingWalkNodeId,
      },
      scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
      scheduleItemKey: `${label}||Exhibit`,
      viewingWalkNodeId,
   };
}
