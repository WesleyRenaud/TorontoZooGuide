import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import {
   MAP_SVG_PATH,
   MIN_FILE_SIZE_BYTES,
   REQUIRED_FRAGMENTS,
   SUSPICIOUS_TRUNCATION_SIZE_BYTES,
   validateMapSvg,
} from '../../tools/lint/mapSvgIntegrity.js';

test( 'validateMapSvg accepts the committed zoo map SVG', () => {
   const violations = validateMapSvg( MAP_SVG_PATH );

   assert.deepEqual( violations, [] );
} );

test( 'validateMapSvg reports truncation and missing fragments', () => {
   const tempDir = fs.mkdtempSync( path.join( os.tmpdir(), 'tzg-map-svg-' ) );
   const tempPath = path.join( tempDir, 'broken.svg' );
   const content = [
      '<svg xmlns="http://www.w3.org/2000/svg">',
      '<defs>',
      '<image id="image38_2_6"/>',
      '</defs>',
      '</svg>',
   ].join( '' );

   fs.writeFileSync( tempPath, content );

   const violations = validateMapSvg( tempPath );

   assert.ok(
      violations.some( violation => violation.includes( 'below minimum expected' ) )
   );
   assert.ok(
      violations.some( violation => violation.includes( 'image39_2_6' ) )
   );
   assert.ok(
      violations.some( violation => violation.includes( 'zoomobile-route-winter' ) )
   );
} );

test( 'validateMapSvg reports the known 8 MB truncation size', () => {
   const tempDir = fs.mkdtempSync( path.join( os.tmpdir(), 'tzg-map-svg-' ) );
   const tempPath = path.join( tempDir, 'truncated.svg' );
   const padding = 'x'.repeat(
      SUSPICIOUS_TRUNCATION_SIZE_BYTES - '</svg>'.length
   );

   fs.writeFileSync( tempPath, `${ padding }</svg>` );

   const violations = validateMapSvg( tempPath );

   assert.ok(
      violations.some( violation => violation.includes( 'known truncation limit' ) )
   );
   assert.ok(
      violations.some( violation => violation.includes( 'below minimum expected' ) )
   );
} );

test( 'validateMapSvg reports a missing closing svg tag', () => {
   const tempDir = fs.mkdtempSync( path.join( os.tmpdir(), 'tzg-map-svg-' ) );
   const tempPath = path.join( tempDir, 'unclosed.svg' );
   const content = `<svg>${ REQUIRED_FRAGMENTS.join( '' ) }`;

   fs.writeFileSync( tempPath, content.padEnd( MIN_FILE_SIZE_BYTES + 1, 'x' ) );

   const violations = validateMapSvg( tempPath );

   assert.ok(
      violations.some( violation => violation === 'file does not end with </svg>' )
   );
} );
