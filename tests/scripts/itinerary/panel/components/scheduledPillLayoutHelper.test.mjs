import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduledItem } from '../../../helpers/scheduledPillTestSetup.mjs';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';
import { ScheduledPillChecker } from '../../../../../scripts/itinerary/panel/components/scheduledPillChecker.js';
import { ScheduledPillLayoutHelper } from '../../../../../scripts/itinerary/panel/components/scheduledPillLayoutHelper.js';

function _attractionItem(label, startMinutes, maximumDuration = 2, anchorSlotMinutes = 570) {
   return {
      ...makeScheduledItem(label, startMinutes, maximumDuration, anchorSlotMinutes),
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      item: { name: label },
   };
}

function _nonModuleItem(label, startMinutes, maximumDuration = 2) {
   return {
      ...makeScheduledItem(label, startMinutes, maximumDuration),
      scheduleItemKind: 'entrance',
   };
}

test('Test_GetScheduledPillMinDisplayMinutes_TestMatchesTheClusteringThreshold_ExpectOk', () => {
   assert.ok(ScheduledPillChecker.getScheduledPillMinDisplayMinutes() > 2.9);
   assert.ok(ScheduledPillChecker.getScheduledPillMinDisplayMinutes() < 3.1);
});

test('Test_ClusterShortScheduledItemsForDisplay_TestGroupsShortVisitsUntilDisplaySpanIsFilled_ExpectOk', () => {
   const clusteredItems = ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 2, 570),
      makeScheduledItem('Red Panda', 582, 2, 570),
   ], 8);

   assert.equal(clusteredItems.length, 2);
   assert.equal(clusteredItems[0].label, 'Babirusa + 1');
   assert.equal(clusteredItems[1].label, 'Red Panda');
});

test('Test_ClusterShortScheduledItemsForDisplay_TestPullsTheNextVisitIntoAnUnderMinPill_ExpectOk', () => {
   const clusteredItems = ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 8, 570),
      makeScheduledItem('Greater One-Horned Rhinoceros', 580, 8, 570),
   ]);

   assert.equal(clusteredItems.length, 2);
   assert.equal(clusteredItems[0].label, 'Cheetah + 1');
   assert.equal(clusteredItems[1].label, 'Greater One-Horned Rhinoceros');
});

test('Test_ClusterShortScheduledItemsForDisplay_TestKeepsReadableVisitsSeparate_ExpectOk', () => {
   const clusteredItems = ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Babirusa', 570, 30, 570),
      makeScheduledItem('Cheetah', 574, 30, 570),
      makeScheduledItem('Red Panda', 575, 30, 570),
   ]);

   assert.equal(clusteredItems.length, 3);
   assert.equal(clusteredItems[0].label, 'Babirusa');
   assert.equal(clusteredItems[1].label, 'Cheetah');
   assert.equal(clusteredItems[2].label, 'Red Panda');
});

test('Test_ClusterShortScheduledItemsForDisplay_TestOrdersGroupedAnimalsByMaxDuration_ExpectOk', () => {
   const clusteredItems = ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Lake Malawi Cichlid', 570, 2, 570),
      makeScheduledItem('Masai Giraffe', 572, 8, 570),
   ], 8);

   assert.equal(clusteredItems.length, 1);
   assert.equal(clusteredItems[0].label, 'Masai Giraffe + 1');
   assert.deepEqual(
      clusteredItems[0].clusterItems.map((item) => item.label),
      [
         'Masai Giraffe',
         'Lake Malawi Cichlid',
      ]
   );
});

test('Test_GetScheduledItemDurationMinutes_TestMissingEnd_ExpectMaximumDuration', () => {
   assert.equal(
      ScheduledPillLayoutHelper.getScheduledItemDurationMinutes({
         startMinutes: 570,
         maximumDuration: 12,
      }),
      12
   );
   assert.equal(ScheduledPillLayoutHelper.getClusterWallSpanMinutes([]), 0);
});

test('Test_MergeLayoutUnits_TestCarouselAndSingle_ExpectMerged', () => {
   const left = makeScheduledItem('Lion', 570, 2);
   const right = makeScheduledItem('Tiger', 572, 2);

   assert.equal(ScheduledPillLayoutHelper.isCarouselMergeableItem(left), true);
   assert.equal(ScheduledPillLayoutHelper.canMergeCarouselLayoutUnits(left, right), true);
   assert.equal(
      ScheduledPillLayoutHelper.canMergeCarouselLayoutUnits(left, _nonModuleItem('Gate', 574)),
      false
   );

   const merged = ScheduledPillLayoutHelper.mergeLayoutUnits(left, right);
   assert.ok(merged.clusterItems);
   assert.equal(merged.clusterItems.length, 2);
   assert.equal(
      ScheduledPillLayoutHelper.mergeLayoutUnits(left, { clusterItems: [] }).label,
      'Lion'
   );
});

test('Test_LayoutUnitAccessors_TestStartsEndsAndUnderMin_ExpectComputed', () => {
   const first = makeScheduledItem('Lion', 570, 2);
   const second = makeScheduledItem('Tiger', 572, 2);

   assert.equal(ScheduledPillLayoutHelper.getLayoutUnitStartMinutes(first), 570);
   assert.equal(ScheduledPillLayoutHelper.getLayoutUnitEndMinutes(first), 572);
   assert.equal(ScheduledPillLayoutHelper.getLayoutUnitWallSpanMinutes(first), 2);
   assert.equal(ScheduledPillLayoutHelper.areConsecutiveLayoutUnits(first, second), true);
   assert.equal(ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(first, 8), true);
   assert.equal(ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(
      makeScheduledItem('Long', 570, 30),
      8
   ), false);
});

test('Test_UnderMinLayoutUnitsNeedMerge_TestOverlapWindows_ExpectMergeFlags', () => {
   const left = makeScheduledItem('Lion', 570, 2);
   const nearRight = makeScheduledItem('Tiger', 574, 2);
   const farRight = makeScheduledItem('Bear', 590, 2);

   assert.equal(
      ScheduledPillLayoutHelper.underMinLayoutUnitsNeedMerge(left, nearRight, 8),
      true
   );
   assert.equal(
      ScheduledPillLayoutHelper.underMinLayoutUnitsNeedMerge(left, farRight, 8),
      false
   );
   assert.equal(
      ScheduledPillLayoutHelper.underMinLayoutUnitsNeedMerge(
         { startMinutes: Number.NaN },
         nearRight,
         8
      ),
      false
   );
});

test('Test_MergeConsecutiveAndUnderMinDisplayLayoutUnits_TestShortChain_ExpectMerged', () => {
   const units = [
      makeScheduledItem('Lion', 570, 2),
      makeScheduledItem('Tiger', 572, 2),
      makeScheduledItem('Bear', 580, 2),
   ];

   const consecutive = ScheduledPillLayoutHelper.mergeConsecutiveUnderMinDisplayLayoutUnits(units, 8);
   assert.equal(consecutive.length, 2);

   const underMin = ScheduledPillLayoutHelper.mergeUnderMinDisplayLayoutUnits([
      makeScheduledItem('A', 570, 2),
      makeScheduledItem('B', 574, 2),
      makeScheduledItem('C', 590, 2),
   ], 8);
   assert.equal(underMin.changed, true);
   assert.ok(underMin.layoutUnits.length < 3);

   const absorbPrevious = ScheduledPillLayoutHelper.mergeUnderMinDisplayLayoutUnits([
      makeScheduledItem('Long', 570, 10),
      makeScheduledItem('Short', 578, 2),
   ], 8);
   assert.equal(absorbPrevious.changed, true);
});

test('Test_AbsorbHeadAndTailOrphanLayoutUnits_TestOrphans_ExpectAbsorbed', () => {
   const head = [
      makeScheduledItem('Short', 570, 2),
      makeScheduledItem('Next', 572, 10),
   ];
   const absorbedHead = ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(head, 8);
   assert.equal(absorbedHead.length, 1);

   assert.deepEqual(
      ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits([makeScheduledItem('Alone', 570, 2)], 8),
      [makeScheduledItem('Alone', 570, 2)]
   );

   const nonConsecutiveHead = [
      makeScheduledItem('Short', 570, 2),
      makeScheduledItem('Gap', 580, 10),
   ];
   assert.deepEqual(
      ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(nonConsecutiveHead, 8),
      nonConsecutiveHead
   );

   const nonMergeableHead = [
      makeScheduledItem('Short', 570, 2),
      _nonModuleItem('Gate', 572, 10),
   ];
   assert.deepEqual(
      ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(nonMergeableHead, 8),
      nonMergeableHead
   );

   const longHead = [
      makeScheduledItem('Long', 570, 10),
      makeScheduledItem('Next', 580, 10),
   ];
   assert.deepEqual(
      ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(longHead, 8),
      longHead
   );

   const tailOrphan = {
      ...makeScheduledItem('Tail', 595, 2, 570),
      slotEndMinutes: 600,
   };
   assert.equal(ScheduledPillLayoutHelper.isTailOrphanLayoutUnit(tailOrphan, 8), true);
   assert.equal(
      ScheduledPillLayoutHelper.isTailOrphanLayoutUnit(makeScheduledItem('Long', 570, 30), 8),
      false
   );
   assert.equal(
      ScheduledPillLayoutHelper.isTailOrphanLayoutUnit({
         ...makeScheduledItem('NoSlot', 570, 2),
         slotEndMinutes: undefined,
         anchorSlotMinutes: undefined,
      }, 8),
      false
   );

   const absorbedTail = ScheduledPillLayoutHelper.absorbTailOrphanLayoutUnits([
      makeScheduledItem('Prev', 570, 10),
      tailOrphan,
   ], 8);
   assert.equal(absorbedTail.length, 1);

   assert.deepEqual(
      ScheduledPillLayoutHelper.absorbTailOrphanLayoutUnits([
         _nonModuleItem('Gate', 570, 10),
         tailOrphan,
      ], 8).map((item) => item.label),
      ['Gate', 'Tail']
   );
});

test('Test_GetEarliestAndAnimalGrouping_TestWalkNodes_ExpectClustered', () => {
   assert.equal(ScheduledPillLayoutHelper.getEarliestScheduledItemByStartTime([]), null);
   assert.equal(ScheduledPillLayoutHelper.isAnimalScheduledItem(makeScheduledItem('Lion', 570)), true);
   assert.equal(
      ScheduledPillLayoutHelper.areAdjacentOrOverlappingScheduledItems(
         makeScheduledItem('Lion', 570, 10),
         makeScheduledItem('Tiger', 575, 10)
      ),
      true
   );
   assert.equal(
      ScheduledPillLayoutHelper.areAdjacentOrOverlappingScheduledItems(
         { startMinutes: Number.NaN },
         makeScheduledItem('Tiger', 575)
      ),
      false
   );

   const sharedNodeA = makeScheduledItem('Lion', 570, 10, 570, 'node-1');
   const sharedNodeB = makeScheduledItem('Tiger', 575, 10, 570, 'node-1');
   const otherKind = _attractionItem('Carousel', 580, 10);
   assert.equal(
      ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(sharedNodeA, sharedNodeB),
      true
   );
   assert.equal(
      ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(sharedNodeA, otherKind),
      false
   );
   assert.equal(
      ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(
         otherKind,
         makeScheduledItem('Bear', 585, 10, 570, 'node-1')
      ),
      false
   );
   assert.equal(
      ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(
         sharedNodeA,
         makeScheduledItem('Bear', 575, 10, 570, '')
      ),
      false
   );
   assert.equal(
      ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(
         sharedNodeA,
         makeScheduledItem('Bear', 575, 10, 570, 'node-2')
      ),
      false
   );

   const clusters = [];
   ScheduledPillLayoutHelper.flushViewingWalkNodeClusterItems([sharedNodeA], clusters);
   ScheduledPillLayoutHelper.flushViewingWalkNodeClusterItems([sharedNodeA, sharedNodeB], clusters);
   assert.equal(clusters.length, 2);
   assert.ok(clusters[1].clusterItems);

   assert.equal(
      ScheduledPillLayoutHelper.compareScheduledItemsForLayout(
         makeScheduledItem('B', 570),
         makeScheduledItem('A', 570)
      ) > 0,
      true
   );

   const walkClusters = ScheduledPillLayoutHelper.clusterScheduledAnimalItemsByViewingWalkNode([
      sharedNodeB,
      sharedNodeA,
      makeScheduledItem('Solo', 600, 10, 600, 'node-9'),
      makeScheduledItem('Join', 605, 10, 600, 'node-9'),
   ]);
   assert.ok(walkClusters.some((item) => item.clusterItems?.length === 2));

   // Last single item does not overlap the next visit, but the flushed cluster wall does.
   const rejoinClusters = ScheduledPillLayoutHelper.clusterScheduledAnimalItemsByViewingWalkNode([
      makeScheduledItem('Long', 570, 30, 570, 'node-rejoin'),
      makeScheduledItem('Short', 580, 5, 570, 'node-rejoin'),
      makeScheduledItem('Rejoin', 590, 10, 570, 'node-rejoin'),
   ]);
   assert.equal(rejoinClusters.length, 1);
   assert.equal(rejoinClusters[0].clusterItems?.length, 3);
});

test('Test_NormalizeLayoutUnitsForDisplay_TestUnderMinChain_ExpectNormalized', () => {
   const normalized = ScheduledPillLayoutHelper.normalizeLayoutUnitsForDisplay([
      makeScheduledItem('A', 570, 2),
      makeScheduledItem('B', 572, 2),
      makeScheduledItem('C', 574, 2),
   ], 8);

   assert.equal(normalized.length, 1);
});

test('Test_ClusterScheduledItemsByDuration_TestAlias_ExpectDelegates', () => {
   const items = [
      makeScheduledItem('Babirusa', 570, 2, 570),
      makeScheduledItem('Cheetah', 572, 2, 570),
   ];
   const byDuration = ScheduledPillLayoutHelper.clusterScheduledItemsByDuration(items, 8);
   const byAlias = ScheduledPillLayoutHelper.clusterScheduledItemsByStartTimeProximity(items, 8);

   assert.equal(byDuration.length, 1);
   assert.deepEqual(byAlias.map((item) => item.label), byDuration.map((item) => item.label));
});

test('Test_DurationAndWallSpanHelpers_TestFallbacks_ExpectValues', () => {
   assert.equal(
      ScheduledPillLayoutHelper.getScheduledItemDurationMinutes({
         startMinutes: Number.NaN,
         maximumDuration: 12,
      }),
      12
   );
   assert.equal(ScheduledPillLayoutHelper.getClusterWallSpanMinutes([]), 0);
   assert.equal(
      ScheduledPillLayoutHelper.getClusterWallSpanMinutes([
         makeScheduledItem('A', 570, 10),
         makeScheduledItem('B', 575, 10),
      ]),
      15
   );
});

test('Test_MergeLayoutUnits_TestSingleItem_ExpectItem', () => {
   const item = _attractionItem('Carousel', 570, 10);
   const merged = ScheduledPillLayoutHelper.mergeLayoutUnits(item, {
      clusterItems: [],
      startMinutes: 580,
      maximumDuration: 0,
   });

   // when right contributes nothing useful, still returns cluster or item
   assert.ok(merged);
});

test('Test_UnderMinLayoutUnitsNeedMerge_TestNonFinite_ExpectFalse', () => {
   assert.equal(
      ScheduledPillLayoutHelper.underMinLayoutUnitsNeedMerge(
         { startMinutes: Number.NaN },
         makeScheduledItem('B', 572, 2)
      ),
      false
   );
});

test('Test_AbsorbHeadOrphanLayoutUnits_TestNonMergeable_ExpectUnchanged', () => {
   const units = [
      _nonModuleItem('Gate', 570, 2),
      _attractionItem('Carousel', 572, 10),
   ];
   assert.deepEqual(
      ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(units, 8),
      units
   );
});

test('Test_IsTailOrphanAndAbsorb_TestSlotEnd_ExpectMergedOrKept', () => {
   const orphan = {
      ...makeScheduledItem('Tail', 598, 2, 570),
      slotEndMinutes: 600,
   };
   assert.equal(ScheduledPillLayoutHelper.isTailOrphanLayoutUnit(orphan, 8), true);

   const absorbed = ScheduledPillLayoutHelper.absorbTailOrphanLayoutUnits([
      _attractionItem('Carousel', 570, 20),
      orphan,
   ], 8);
   assert.ok(Array.isArray(absorbed));
});

test('Test_GetEarliestScheduledItemByStartTime_TestEmptyAndItems_ExpectEarliest', () => {
   assert.equal(ScheduledPillLayoutHelper.getEarliestScheduledItemByStartTime([]), null);
   assert.equal(
      ScheduledPillLayoutHelper.getEarliestScheduledItemByStartTime([
         makeScheduledItem('Late', 600, 10),
         makeScheduledItem('Early', 570, 10),
      ]).label,
      'Early'
   );
});

test('Test_CanGroupScheduledItemsByViewingWalkNode_TestNonAnimalPrevious_ExpectFalse', () => {
   assert.equal(
      ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(
         _attractionItem('Carousel', 570, 10),
         makeScheduledItem('Lion', 575, 10, 570, 'node-1')
      ),
      false
   );
});

test('Test_ClusterScheduledAnimalItemsByViewingWalkNode_TestRejoinFlushedCluster_ExpectMerged', () => {
   const longFirst = makeScheduledItem('Long', 570, 30, 570, 'node-1');
   const shortSecond = makeScheduledItem('Short', 580, 5, 570, 'node-1');
   const overlapsCluster = makeScheduledItem('Rejoin', 590, 10, 570, 'node-1');

   const clusters = ScheduledPillLayoutHelper.clusterScheduledAnimalItemsByViewingWalkNode([
      longFirst,
      shortSecond,
      overlapsCluster,
   ]);

   assert.equal(clusters.length, 1);
   assert.equal(clusters[0].clusterItems?.length, 3);
});
