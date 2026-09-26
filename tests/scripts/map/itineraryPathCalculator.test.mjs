import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryPathRenderer } from '../../../scripts/map/itineraryPathRenderer.js';
import { ItineraryPathCalculator } from '../../../scripts/map/itineraryPathCalculator.js';
import { SvgPathParser } from '../../../scripts/map/svgPathParser.js';
import { WalkGraphPathCalculator } from '../../../scripts/map/walkGraphPathCalculator.js';
import { Position } from '../../../scripts/shared/enums/position.js';

const start = { x: 2515.53, y: 2434.92 };
const curveEnd = { x: 2511.03, y: 2411.92 };
const sourcePathD = `M${start.x} ${start.y}C${start.x} ${start.y} 2513.03 2420.85 ${curveEnd.x} ${curveEnd.y}`;


test('Test_ParseSvgPathD_TestMoveAndCubic_ExpectParsedSegments', () => {
   const segments = SvgPathParser.parseSvgPathD(sourcePathD);

   assert.equal(segments.length, 2);
   assert.equal(segments.at(Position.FIRST).tag, 'M');
   assert.equal(segments.at(Position.SECOND).tag, 'C');
   assert.equal(segments.at(Position.SECOND).x, curveEnd.x);
   assert.equal(segments.at(Position.SECOND).y, curveEnd.y);
});


test('Test_BuildPathDFromWalkGraphSegments_TestSourceCurve_ExpectReusedGeometry', () => {
   const segments = SvgPathParser.parseSvgPathD(sourcePathD);

   const pathD = WalkGraphPathCalculator.buildPathDFromWalkGraphSegments(segments, [
      start,
      curveEnd,
   ]);

   assert.equal(
      pathD,
      `M ${start.x} ${start.y} C ${start.x} ${start.y} 2513.03 2420.85 ${curveEnd.x} ${curveEnd.y}`
   );
});


test('Test_BuildSmoothedPathD_TestThreePoints_ExpectCubicPath', () => {
   const origin = { x: 0, y: 0 };
   const mid = { x: 100, y: 0 };
   const end = { x: 100, y: 100 };

   const pathD = ItineraryPathCalculator.buildSmoothedPathD([origin, mid, end]);

   assert.match(pathD, new RegExp(`^M ${origin.x} ${origin.y} C .+ ${end.x} ${end.y}$`));
});


test('Test_BuildSmoothedPathD_TestTwoPoints_ExpectLine', () => {
   const first = { x: 10, y: 20 };
   const second = { x: 30, y: 40 };

   const pathD = ItineraryPathCalculator.buildSmoothedPathD([first, second]);

   assert.equal(pathD, `M ${first.x} ${first.y} L ${second.x} ${second.y}`);
});


test('Test_BuildPathArrowPlacements_TestStraightPath_ExpectSpacedArrows', () => {
   const expectedCount = 6;
   const firstX = 60;

   const placements = ItineraryPathRenderer.buildPathArrowPlacements('M 0 0 L 400 0');

   assert.equal(placements.length, expectedCount);
   assert.equal(placements.at(Position.FIRST).x, firstX);
   assert.equal(placements.at(Position.FIRST).angleDeg, 0);
});


test('Test_BuildPathArrowPlacements_TestShortPath_ExpectEmpty', () => {
   const placements = ItineraryPathRenderer.buildPathArrowPlacements('M 0 0 L 20 0');

   assert.deepEqual(placements, []);
});


test('Test_BuildItineraryPathDFromWalkLegs_TestTransitGaps_ExpectDiscontinuous', () => {
   const first = { nodeId: 'a', x: 0, y: 0 };
   const second = { nodeId: 'b', x: 10, y: 0 };
   const third = { nodeId: 'c', x: 100, y: 100 };
   const fourth = { nodeId: 'd', x: 110, y: 100 };

   const pathD = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
      [
         { nodeIds: [first.nodeId, second.nodeId] },
         { nodeIds: [third.nodeId, fourth.nodeId] },
      ],
      [first, second, third, fourth],
      {
         pointToMapPx: (point) => ({ x: point.x, y: point.y }),
      }
   );

   assert.equal(
      pathD,
      `M ${first.x} ${first.y} L ${second.x} ${second.y} M ${third.x} ${third.y} L ${fourth.x} ${fourth.y}`
   );
});


test('Test_BuildItineraryPathDFromWalkLegs_TestTransitStation_ExpectContinuousLeg', () => {
   const exhibit = { nodeId: 'exhibit', x: 0, y: 0 };
   const path = { nodeId: 'path', x: 10, y: 0 };
   const domainStation = { nodeId: 'domain-station', x: 20, y: 0 };
   const africaStation = { nodeId: 'africa-station', x: 200, y: 200 };
   const nextExhibit = { nodeId: 'next-exhibit', x: 210, y: 200 };

   const pathD = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
      [
         { nodeIds: [exhibit.nodeId, path.nodeId, domainStation.nodeId] },
         { nodeIds: [africaStation.nodeId, nextExhibit.nodeId] },
      ],
      [exhibit, path, domainStation, africaStation, nextExhibit],
      {
         pointToMapPx: (point) => ({ x: point.x, y: point.y }),
      }
   );

   assert.match(
      pathD,
      new RegExp(`^M ${exhibit.x} ${exhibit.y}[\\s\\S]*${domainStation.x} ${domainStation.y} M ${africaStation.x} ${africaStation.y} L ${nextExhibit.x} ${nextExhibit.y}$`)
   );
   assert.equal(pathD.includes(`L ${africaStation.x} ${africaStation.y}`), false);
});


test('Test_BuildSmoothedPathD_TestEmpty_ExpectEmpty', () => {
   const pathD = ItineraryPathCalculator.buildSmoothedPathD([]);

   assert.equal(pathD, '');
});


test('Test_BuildSmoothedPathD_TestSinglePoint_ExpectEmpty', () => {
   const pathD = ItineraryPathCalculator.buildSmoothedPathD([{ x: 1, y: 1 }]);

   assert.equal(pathD, '');
});


test('Test_BuildExactPathD_TestSinglePoint_ExpectEmpty', () => {
   const pathD = ItineraryPathCalculator.buildExactPathD([{ x: 1, y: 1 }]);

   assert.equal(pathD, '');
});


test('Test_BuildExactPathD_TestPoints_ExpectPolyline', () => {
   const first = { x: 0, y: 0 };
   const mid = { x: 5, y: 5 };
   const last = { x: 10, y: 0 };

   const pathD = ItineraryPathCalculator.buildExactPathD([first, mid, last]);

   assert.equal(pathD, `M ${first.x} ${first.y} L ${mid.x} ${mid.y} L ${last.x} ${last.y}`);
});


test('Test_BuildRouteMapPoints_TestSinglePoint_ExpectEmpty', () => {
   const points = ItineraryPathCalculator.buildRouteMapPoints([{ x: 1, y: 1 }], {
      withEntranceLandmark: (nextPoints) => nextPoints,
   });

   assert.deepEqual(points, []);
});


test('Test_BuildRouteMapPoints_TestFilterAndEntrance_ExpectMapped', () => {
   const entrance = { x: 0, y: 0 };
   const kept = { x: 2, y: 2 };
   const scale = 10;

   const points = ItineraryPathCalculator.buildRouteMapPoints(
      [{ x: 1, y: 1 }, kept],
      {
         withEntranceLandmark: (nextPoints) => [entrance, ...nextPoints],
         pointToMapPx: (point) => (point.x === 1 ? null : { x: point.x * scale, y: point.y * scale }),
      }
   );

   assert.deepEqual(points, [
      entrance,
      { x: kept.x * scale, y: kept.y * scale },
   ]);
});


test('Test_BuildItineraryPathD_TestSinglePoint_ExpectEmpty', () => {
   const pathD = ItineraryPathCalculator.buildItineraryPathD([{ x: 0, y: 0 }]);

   assert.equal(pathD, '');
});


test('Test_BuildItineraryPathD_TestWalkGraph_ExpectPath', () => {
   const routePoints = [
      { x: 0, y: 0 },
      { x: 10, y: 0 },
   ];
   const walkPath = 'M 0 0 L 10 0';
   const originalGet = WalkGraphPathCalculator.getWalkGraphPathSegments;
   const originalBuild = WalkGraphPathCalculator.buildPathDFromWalkGraphSegments;
   WalkGraphPathCalculator.getWalkGraphPathSegments = () => [{ tag: 'M' }];
   WalkGraphPathCalculator.buildPathDFromWalkGraphSegments = () => walkPath;

   try {
      const pathD = ItineraryPathCalculator.buildItineraryPathD(routePoints);

      assert.equal(pathD, walkPath);
   } finally {
      WalkGraphPathCalculator.getWalkGraphPathSegments = originalGet;
      WalkGraphPathCalculator.buildPathDFromWalkGraphSegments = originalBuild;
   }
});


test('Test_BuildItineraryPathD_TestFallback_ExpectExact', () => {
   const routePoints = [
      { x: 0, y: 0 },
      { x: 10, y: 0 },
   ];

   const pathD = ItineraryPathCalculator.buildItineraryPathD(routePoints, []);

   assert.equal(pathD, ItineraryPathCalculator.buildExactPathD(routePoints));
});


test('Test_BuildItineraryPathDFromWalkLegs_TestEmptyLegs_ExpectEmpty', () => {
   const pathD = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs([], [{ x: 0, y: 0 }]);

   assert.equal(pathD, '');
});


test('Test_BuildItineraryPathDFromWalkLegs_TestSharedJoin_ExpectStart', () => {
   const sharedPath = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
      [
         { nodeIds: ['a', 'b'] },
         { nodeIds: ['b', 'c'] },
      ],
      [
         { nodeId: 'a', x: 0, y: 0 },
         { nodeId: 'b', x: 10, y: 0 },
         { nodeId: 'c', x: 20, y: 0 },
      ]
   );

   assert.match(sharedPath, /M 0 0/);
});


test('Test_BuildItineraryPathDFromWalkLegs_TestMissingNode_ExpectEmpty', () => {
   const pathD = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
      [{ nodeIds: ['a', 'b', 'c'] }],
      [
         { nodeId: 'a', x: 0, y: 0 },
         { nodeId: 'b', x: 10, y: 0 },
      ]
   );

   assert.equal(pathD, '');
});


test('Test_BuildItineraryPathDFromWalkLegs_TestUnmappedPoint_ExpectEmpty', () => {
   const pathD = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
      [{ nodeIds: ['a', 'b'] }],
      [
         { nodeId: 'a', x: 0, y: 0 },
         { nodeId: 'b', x: 10, y: 0 },
      ],
      {
         pointToMapPx: (point) => (point.nodeId === 'b' ? null : point),
      }
   );

   assert.equal(pathD, '');
});


test('Test_BuildItineraryPathDFromWalkLegs_TestSingleNode_ExpectEmpty', () => {
   const pathD = ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
      [{ nodeIds: ['a'] }],
      [{ nodeId: 'a', x: 0, y: 0 }]
   );

   assert.equal(pathD, '');
});
