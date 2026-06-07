import assert from 'node:assert/strict';
import { test } from 'node:test';

import { buildScheduledItemRowsContext, buildScheduledItinerary } from '../../scripts/itinerary/panel/dayPlannerScheduledItems.js';
import {
   resolveGroupedScheduledPillOptions,
   resolveScheduledPillOptions,
} from '../../scripts/itinerary/panel/components/dayPlannerTimelinePills.js';
import {
   clusterScheduledItemsByDuration,
   clusterShortScheduledItemsForDisplay,
   computeFirstFreeHorizontalOffsetIndex,
   doScheduledTimeRangesOverlap,
   formatScheduledPillGroupLabel,
   MAX_TIMELINE_PILL_COLUMNS,
   MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS,
   getScheduledItemEndMinutes,
   getScheduledPillMinDisplayMinutes,
   planScheduledPillRenderGroupsByAnchor,
   scheduledPillsOverlapInDefaultPosition,
} from '../../scripts/itinerary/panel/components/dayPlannerTimelinePillOverlap.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';

function makeScheduledItem(label, startMinutes, maximumDuration = 30, anchorSlotMinutes = 570) {
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
      },
      scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
      scheduleItemKey: `${label}||Exhibit`,
   };
}

test('getScheduledItemEndMinutes uses parsed endMinutes from schedule times', () => {
   assert.equal(
      getScheduledItemEndMinutes({
         startMinutes: 600,
         maximumDuration: 8,
         endMinutes: 615,
      }),
      615
   );
   assert.ok(Number.isNaN(getScheduledItemEndMinutes({
      startMinutes: 600,
      maximumDuration: 8,
   })));
});

test('doScheduledTimeRangesOverlap uses strict bounds for touching windows', () => {
   assert.equal(
      doScheduledTimeRangesOverlap(
         { startMinutes: 570, endMinutes: 600 },
         { startMinutes: 590, endMinutes: 620 }
      ),
      true
   );
   assert.equal(
      doScheduledTimeRangesOverlap(
         { startMinutes: 570, endMinutes: 600 },
         { startMinutes: 600, endMinutes: 630 }
      ),
      false
   );
});

test('scheduledPillsOverlapInDefaultPosition detects overlap within a slot', () => {
   assert.equal(
      scheduledPillsOverlapInDefaultPosition(
         makeScheduledItem('Babirusa', 570, 30),
         makeScheduledItem('Cheetah', 575, 30)
      ),
      true
   );
});

test('scheduledPillsOverlapInDefaultPosition ignores back-to-back slot boundaries', () => {
   assert.equal(
      scheduledPillsOverlapInDefaultPosition(
         makeScheduledItem('Babirusa', 570, 30, 570),
         makeScheduledItem('Greater One-Horned Rhinoceros', 600, 30, 600)
      ),
      false
   );
});

test('computeFirstFreeHorizontalOffsetIndex reuses open columns', () => {
   const placedItems = [
      { ...makeScheduledItem('Babirusa', 570, 30), horizontalOffsetIndex: 0 },
      { ...makeScheduledItem('Red Panda', 630, 30), horizontalOffsetIndex: 2 },
   ];

   assert.equal(
      computeFirstFreeHorizontalOffsetIndex(
         placedItems,
         makeScheduledItem('Cheetah', 575, 30)
      ),
      1
   );
});

test('planScheduledPillRenderGroupsByAnchor keeps sequential visits in column zero', () => {
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Babirusa', 570, 30, 570),
      makeScheduledItem('Greater One-Horned Rhinoceros', 600, 30, 600),
      makeScheduledItem('Indian Peafowl', 630, 30, 630),
   ]);

   assert.deepEqual(
      groupsByAnchor.get(570)?.map((group) => group.horizontalOffsetIndex),
      [ 0 ]
   );
   assert.deepEqual(
      groupsByAnchor.get(600)?.map((group) => group.horizontalOffsetIndex),
      [ 0 ]
   );
});

test('getScheduledPillMinDisplayMinutes matches the clustering threshold', () => {
   assert.ok(getScheduledPillMinDisplayMinutes() > 2.9);
   assert.ok(getScheduledPillMinDisplayMinutes() < 3.1);
});

test('clusterShortScheduledItemsForDisplay groups short visits until display span is filled', () => {
   const clusteredItems = clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 2, 570),
      makeScheduledItem('Red Panda', 582, 2, 570),
   ], 8);

   assert.equal(clusteredItems.length, 2);
   assert.equal(clusteredItems[0].label, 'Babirusa + 1');
   assert.equal(clusteredItems[1].label, 'Red Panda');
});

test('clusterShortScheduledItemsForDisplay pulls the next visit into an under-min pill', () => {
   const clusteredItems = clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 8, 570),
      makeScheduledItem('Greater One-Horned Rhinoceros', 580, 8, 570),
   ]);

   assert.equal(clusteredItems.length, 2);
   assert.equal(clusteredItems[0].label, 'Babirusa + 1');
   assert.equal(clusteredItems[1].label, 'Greater One-Horned Rhinoceros');
});

test('clusterShortScheduledItemsForDisplay keeps readable visits separate', () => {
   const clusteredItems = clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 30, 570),
      makeScheduledItem('Cheetah', 574, 30, 570),
      makeScheduledItem('Red Panda', 575, 30, 570),
   ]);

   assert.equal(clusteredItems.length, 3);
   assert.equal(clusteredItems[0].label, 'Babirusa');
   assert.equal(clusteredItems[1].label, 'Cheetah');
   assert.equal(clusteredItems[2].label, 'Red Panda');
});

test('planScheduledPillRenderGroupsByAnchor clusters short visits in the same slot', () => {
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 2, 570),
   ]);

   assert.equal(groupsByAnchor.get(570)?.length, 1);
   assert.equal(groupsByAnchor.get(570)?.[0]?.label, 'Babirusa + 1');
   assert.deepEqual(
      groupsByAnchor.get(570)?.map((group) => group.horizontalOffsetIndex),
      [ 0 ]
   );
});

test('planScheduledPillRenderGroupsByAnchor keeps consecutive time buckets visible', () => {
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Eurasian Eagle Owl', 990, 2, 990),
      makeScheduledItem('Great Horned Owl', 992, 2, 990),
      makeScheduledItem('Guinea Pig', 994, 1, 990),
      makeScheduledItem('Harris Hawk', 995, 1, 990),
      makeScheduledItem('Marabou Stork', 996, 2, 990),
      makeScheduledItem('Rabbit', 998, 2, 990),
      makeScheduledItem('American Flamingo', 1000, 5, 990),
      makeScheduledItem('Black-Handed Spider Monkey', 1005, 5, 990),
      makeScheduledItem('Capybara', 1010, 5, 990),
      makeScheduledItem('Red-Legged Seriema', 1015, 2, 990),
      makeScheduledItem('Turkey Vulture', 1017, 1, 990),
   ]);
   const groupLabels = (groupsByAnchor.get(990) ?? []).map((group) => (
      group.label ?? group.items[0].label
   ));

   assert.deepEqual(groupLabels, [
      'Eurasian Eagle Owl + 1',
      'Guinea Pig + 2',
      'Rabbit + 1',
      'Black-Handed Spider Monkey',
      'Capybara',
      'Red-Legged Seriema + 1',
   ]);
});

test('planScheduledPillRenderGroupsByAnchor leaves no gap between consecutive layout units', () => {
   const slotSpanMinutes = 30;
   const groups = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Clouded Leopard', 570, 30, 570),
      makeScheduledItem('Black Carp', 600, 4, 600),
      makeScheduledItem('Crocodile Lizard', 604, 4, 600),
      makeScheduledItem('Luzon Bleeding-Heart Dove', 608, 4, 600),
      makeScheduledItem('Sumatran Orangutan', 612, 30, 600),
      makeScheduledItem('Tentacled Snake', 642, 4, 600),
      makeScheduledItem('White-Handed Gibbon', 646, 4, 600),
   ]).get(600) ?? [];

   for (let index = 1; index < groups.length; index += 1) {
      const previousGroup = groups[index - 1];
      const previousEndOffset = (previousGroup.offsetFraction ?? 0)
         + ((previousGroup.durationMinutes ?? 0) / slotSpanMinutes);

      assert.ok(
         Math.abs((groups[index]?.offsetFraction ?? 0) - previousEndOffset) < 0.0001,
         `expected group ${index} to start where group ${index - 1} ends`
      );
   }
});

test('planScheduledPillRenderGroupsByAnchor merges gapped under-min clusters into the next group', () => {
   const groups = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Black Carp', 600, 1, 600),
      makeScheduledItem('Black-Breasted Leaf Turtle', 601, 1, 600),
      makeScheduledItem('Burmese Star Tortoise', 603, 1, 600),
      makeScheduledItem('Crested Wood Partridge', 604, 2, 600),
   ]).get(600) ?? [];

   assert.equal(groups.length, 1);
   assert.equal(groups[0]?.label ?? groups[0]?.items[0]?.label, 'Black Carp + 3');
   assert.equal(groups[0]?.durationMinutes, 6);
   assert.equal(groups[0]?.displayDurationMinutes, 6);
});

test('planScheduledPillRenderGroupsByAnchor keeps real gaps after short groups', () => {
   const groups = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Indian Peafowl', 600, 1, 600),
      makeScheduledItem('Luzon Bleeding-Heart Dove', 625, 2, 600),
   ]).get(600) ?? [];

   assert.equal(groups.length, 2);
   assert.deepEqual(
      groups.map((group) => group.label ?? group.items[0].label),
      [
         'Indian Peafowl',
         'Luzon Bleeding-Heart Dove',
      ]
   );
   assert.equal(groups[0]?.durationMinutes, 1);
   assert.equal(groups[0]?.displayDurationMinutes, getScheduledPillMinDisplayMinutes());
   assert.equal(groups[1]?.durationMinutes, 2);
   assert.equal(groups[1]?.displayDurationMinutes, getScheduledPillMinDisplayMinutes());
});

test('planScheduledPillRenderGroupsByAnchor uses start times for pill positions', () => {
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Two-Toed Sloth', 570, 30, 570),
      ...Array.from({ length: 9 }, (_, index) => (
         makeScheduledItem(
            `Fish ${index + 1}`,
            571 + index,
            2,
            570
         )
      )),
   ]);
   const groups = groupsByAnchor.get(570) ?? [];

   assert.equal(groups[0]?.label ?? groups[0]?.items[0]?.label, 'Two-Toed Sloth');
   assert.equal(groups[0]?.offsetFraction ?? 0, 0);

   groups.slice(1).forEach((group) => {
      const firstItem = group.items[0];
      const expectedOffset = (firstItem.startMinutes - 570) / 30;

      assert.ok(
         Math.abs((group.offsetFraction ?? 0) - expectedOffset) < 0.0001,
         `expected ${group.label ?? firstItem.label} at offset ${expectedOffset}`
      );
   });
});

test('planScheduledPillRenderGroupsByAnchor places each slot at its natural start offset', () => {
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Babirusa', 570, 30, 570),
      makeScheduledItem('Cheetah', 571, 30, 570),
      makeScheduledItem('Red Panda', 600, 2, 600),
   ]);
   const nextSlotGroups = groupsByAnchor.get(600) ?? [];

   assert.equal(nextSlotGroups.length, 1);
   assert.equal(nextSlotGroups[0]?.offsetFraction ?? 0, 0);
});

test('planScheduledPillRenderGroupsByAnchor keeps full-length overlapping visits separate', () => {
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Babirusa', 570, 30, 570),
      makeScheduledItem('Cheetah', 576, 30, 570),
   ]);

   assert.equal(groupsByAnchor.get(570)?.length, 2);
   assert.deepEqual(
      groupsByAnchor.get(570)?.map((group) => group.label ?? group.items[0].label),
      [ 'Babirusa', 'Cheetah' ]
   );
   assert.deepEqual(
      groupsByAnchor.get(570)?.map((group) => group.horizontalOffsetIndex),
      [ 0, 0 ]
   );
});

test('planScheduledPillRenderGroupsByAnchor merges a lone tail orphan into the previous cluster', () => {
   const withSlotEnd = (item, slotEndMinutes) => ({ ...item, slotEndMinutes });
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor([
      withSlotEnd(makeScheduledItem('Black-Handed Spider Monkey', 1005, 10, 990), 1020),
      withSlotEnd(makeScheduledItem('Red-Legged Seriema', 1015, 2, 990), 1020),
   ]);
   const groups = groupsByAnchor.get(990) ?? [];

   assert.equal(groups.length, 1);
   assert.equal(groups[0]?.label ?? groups[0]?.items[0]?.label, 'Black-Handed Spider Monkey + 1');
   assert.equal(groups[0]?.durationMinutes, 12);
   assert.equal(groups[0]?.displayDurationMinutes, 12);
});

test('planScheduledPillRenderGroupsByAnchor renders isolated short visits at minimum height', () => {
   const groups = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Greater One-Horned Rhinoceros', 930, 30, 930),
      makeScheduledItem('Black-Throated Laughingthrush', 960, 2, 960),
      makeScheduledItem('Red Panda', 990, 30, 990),
   ]).get(960) ?? [];

   assert.equal(groups.length, 1);
   assert.equal(
      groups[0]?.label ?? groups[0]?.items[0]?.label,
      'Black-Throated Laughingthrush'
   );
   assert.equal(groups[0]?.durationMinutes, 2);
   assert.equal(
      groups[0]?.displayDurationMinutes,
      getScheduledPillMinDisplayMinutes()
   );
});

test('planScheduledPillRenderGroupsByAnchor keeps scheduled pills at full width', () => {
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor(
      [
         makeScheduledItem('Red-Legged Seriema', 1015, 2, 990),
      ],
      [
         { startMinutes: 1020 },
      ]
   );

   assert.deepEqual(
      groupsByAnchor.get(990)?.map((group) => group.horizontalOffsetIndex),
      [ 0 ]
   );
});

test('planScheduledPillRenderGroupsByAnchor merges overlapping visits into carousel groups', () => {
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor([
      makeScheduledItem('Snow Leopard', 971, 8, 960),
      makeScheduledItem('Steller Sea Eagle', 979, 3, 960),
      makeScheduledItem('West Caucasian Tur', 982, 3, 960),
      makeScheduledItem('Domestic Goat', 985, 3, 960),
      makeScheduledItem('African Spurred Tortoise', 988, 1, 960),
      makeScheduledItem('Common Raven', 989, 1, 960),
   ]);
   const groups = groupsByAnchor.get(960) ?? [];

   assert.equal(groups.length, 4);
   assert.deepEqual(
      groups.map((group) => group.label ?? group.items[0].label),
      [
         'Snow Leopard',
         'Steller Sea Eagle',
         'West Caucasian Tur',
         'Domestic Goat + 2',
      ]
   );
   assert.equal(groups[0]?.items.length, 1);
   assert.equal(groups[3]?.items.length, 3);
});

test('planScheduledPillRenderGroupsByAnchor gives each full-length visit its own pill', () => {
   const scheduledItems = [
      'Babirusa',
      'Cheetah',
      'Red Panda',
      'Masai Giraffe',
      'Ostrich',
      'African Lion',
   ].map((label, labelIndex) => (
      makeScheduledItem(label, 570 + labelIndex, 30, 570)
   ));
   const groupsByAnchor = planScheduledPillRenderGroupsByAnchor(scheduledItems);
   const groups = groupsByAnchor.get(570) ?? [];

   assert.equal(groups.length, 6);
   assert.deepEqual(
      groups.map((group) => group.label ?? group.items[0].label),
      [
         'Babirusa',
         'Cheetah',
         'Red Panda',
         'Masai Giraffe',
         'Ostrich',
         'African Lion',
      ]
   );
   assert.equal(MAX_TIMELINE_PILL_COLUMNS, 2);
   assert.equal(MAX_TIMELINE_PILL_INDIVIDUAL_COLUMNS, 2);
});

test('formatScheduledPillGroupLabel matches map-style counted labels', () => {
   assert.equal(
      formatScheduledPillGroupLabel([{ label: 'African Lion' }]),
      'African Lion'
   );
   assert.equal(
      formatScheduledPillGroupLabel([
         { label: 'African Lion' },
         { label: 'Cheetah' },
      ]),
      'African Lion + 1'
   );
});

test('resolveGroupedScheduledPillOptions merges menu actions for grouped pills', () => {
   const options = resolveGroupedScheduledPillOptions(
      [
         makeScheduledItem('African Lion', 570),
         makeScheduledItem('Cheetah', 570),
      ],
      {
         onUnscheduleItineraryItem: () => {},
         onRemoveItineraryItem: () => {},
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   assert.equal(options.menuItems?.length, 4);
});

test('buildScheduledItemRowsContext places generic events on the timeline', () => {
   const context = buildScheduledItemRowsContext(
      {
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         events: [
            {
               event_type: 'lunch',
               start_time: '12:00 PM',
               end_time: '12:40 PM',
            },
         ],
      },
      [720, 750],
      1140
   );
   const lunchItems = [...context.itemsByStart.values()].flat();

   assert.equal(lunchItems.length, 1);
   assert.equal(lunchItems[0].label, 'Lunch');
   assert.equal(lunchItems[0].scheduleItemKind, ScheduleItemKind.EVENT.kind);
   assert.equal(lunchItems[0].scheduleItemEventType, 'lunch');
   assert.equal(lunchItems[0].maximumDuration, 40);
   assert.equal(lunchItems[0].anchorSlotMinutes, 720);
});

test('resolveScheduledPillOptions offers only remove for generic events', () => {
   const removeRequests = [];

   const options = resolveScheduledPillOptions(
      {
         scheduleItemKind: ScheduleItemKind.EVENT.kind,
         scheduleItemEventType: 'lunch',
         scheduleItemKey: '',
      },
      {
         onUnscheduleItineraryItem: () => {
            throw new Error('generic events should not expose unschedule');
         },
         onRemoveItineraryItem: (request) => {
            removeRequests.push(request);
         },
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   assert.equal(options.menuItems?.length, 1);
   assert.equal(options.menuItems?.[0]?.label, 'Remove');

   options.menuItems?.[0]?.onAction?.();

   assert.deepEqual(removeRequests, [{
      itemType: 'lunch',
      key: '',
   }]);
});

test('resolveScheduledPillOptions adds remove for animals and guardians talks', () => {
   const removeRequests = [];

   const animalOptions = resolveScheduledPillOptions(
      {
         scheduleItemKind: 'animals',
         scheduleItemKey: 'African Lion||Africa Savanna',
      },
      {
         onRemoveItineraryItem: (request) => {
            removeRequests.push(request);
         },
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   animalOptions.menuItems?.find((item) => item.label === 'Remove')?.onAction?.();

   assert.deepEqual(removeRequests, [{
      itemType: 'animals',
      key: 'African Lion||Africa Savanna',
   }]);

   const talkOptions = resolveScheduledPillOptions(
      {
         scheduleItemKind: 'guardians_talks',
         scheduleItemKey: 'Amur Tiger',
      },
      {
         onRemoveItineraryItem: (request) => {
            removeRequests.push(request);
         },
      },
      { scheduledItemMenuAria: 'Menu', unschedule: 'Unschedule', remove: 'Remove' }
   );

   assert.equal(talkOptions.menuItems?.length, 1);
   assert.equal(talkOptions.menuItems?.[0]?.label, 'Remove');

   talkOptions.menuItems?.[0]?.onAction?.();

   assert.deepEqual(removeRequests[1], {
      itemType: 'guardians_talks',
      key: 'Amur Tiger',
   });
});

test('buildScheduledItinerary tolerates missing itinerary collections', () => {
   assert.deepEqual(buildScheduledItinerary({}), {
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
});
