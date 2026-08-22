import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

export const MAP_SVG_PATH = path.resolve( 'images/map/zoo-map.svg' );
export const SUSPICIOUS_TRUNCATION_SIZE_BYTES = 8 * 1024 * 1024;
export const MIN_FILE_SIZE_BYTES = 10 * 1024 * 1024;
export const TAIL_READ_BYTES = 500;

export const REQUIRED_FRAGMENTS = [
   'id="image38_2_6"',
   'id="image39_2_6"',
   'id="zoomobile-route-winter"',
   'id="zoomobile-route-summer"',
   'id="zm-w-001"',
   'id="zm-w-241"',
   'id="zm-s-001"',
   'id="zm-s-297"',
   'id="walk-graph" style="display: none;"',
   'id="walk-graph-path"',
   'stroke="black" fill="none"/>',
   '</defs>',
];

function readFileTail( filePath, byteCount ) {
   const fd = fs.openSync( filePath, 'r' );

   try {
      const { size } = fs.fstatSync( fd );
      const start = Math.max( 0, size - byteCount );
      const length = size - start;
      const buffer = Buffer.alloc( length );

      fs.readSync( fd, buffer, 0, length, start );

      return buffer.toString( 'utf8' );
   }
   finally {
      fs.closeSync( fd );
   }
}

export function validateMapSvg(
      filePath,
      {
         readFile = fs.readFileSync,
         stat = fs.statSync,
         exists = fs.existsSync,
      } = {} ) {
   const violations = [];

   if ( !exists( filePath ) ) {
      violations.push( `file not found: ${ filePath }` );
      return violations;
   }

   const { size } = stat( filePath );

   if ( size === SUSPICIOUS_TRUNCATION_SIZE_BYTES ) {
      violations.push(
         `file size is exactly ${ SUSPICIOUS_TRUNCATION_SIZE_BYTES } bytes (known truncation limit)`
      );
   }

   if ( size < MIN_FILE_SIZE_BYTES ) {
      violations.push(
         `file size ${ size } bytes is below minimum expected ${ MIN_FILE_SIZE_BYTES } bytes`
      );
   }

   const head = readFile( filePath, 'utf8' ).slice( 0, 500 );

   if ( !head.includes( '<svg' ) ) {
      violations.push( 'file does not contain an <svg> root element near the start' );
   }

   const tail = readFileTail( filePath, TAIL_READ_BYTES );

   if ( !tail.trimEnd().endsWith( '</svg>' ) ) {
      violations.push( 'file does not end with </svg>' );
   }

   const content = readFile( filePath, 'utf8' );

   for ( const fragment of REQUIRED_FRAGMENTS ) {
      if ( !content.includes( fragment ) ) {
         violations.push( `missing required fragment: ${ fragment }` );
      }
   }

   return violations;
}

function main() {
   const violations = validateMapSvg( MAP_SVG_PATH );

   if ( violations.length === 0 ) {
      return;
   }

   console.error( 'Zoo map SVG integrity check failed for images/map/zoo-map.svg:' );

   violations.forEach( violation => {
      console.error( `  - ${ violation }` );
   } );

   process.exit( 1 );
}

if ( import.meta.url === new URL( process.argv[ 1 ], 'file:' ).href ) {
   main();
}
