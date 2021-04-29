let mymap = L.map("mapid").setView([0, 0], 1);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(mymap);

const options = {
  // See renderer sections below.
  // One of: L.LeafletGeotiff.rgb, L.LeafletGeotiff.plotty, L.LeafletGeotiff.vectorArrows
  renderer: L.LeafletGeotiff.plotty,

  // Optional array specifying the corners of the data, e.g. [[40.712216, -74.22655], [40.773941, -74.12544]].
  // If omitted the image bounds will be read from the geoTIFF file (ModelTiepoint).

  // Optional geoTIFF band to read
  band: 0,

  // Optional geoTIFF image to read
  image: 0,

  // Optional clipping polygon, provided as an array of [lat,lon] coordinates.
  // Note that this is the Leaflet [lat,lon] convention, not geoJSON [lon,lat].
  clip: undefined,

  // Optional leaflet pane to add the layer.
  pane: "overlayPane",

  // Optional callback to handle failed URL request or parsing of tif
  onError: null,

  // Optional, override default GeoTIFF function used to load source data
  // Oneof: fromUrl, fromBlob, fromArrayBuffer
  sourceFunction: GeoTIFF.fromUrl,

  // Only required if sourceFunction is GeoTIFF.fromArrayBuffer
  arrayBuffer: null,

  // Optional nodata value (integer)
  // (to be ignored by getValueAtLatLng)
  noDataValue: undefined,

  // Optional key to extract nodata value from GeoTIFFImage
  // nested keys can be provided in dot notation, e.g. foo.bar.baz
  // (to be ignored by getValueAtLatLng)
  // this overrides noDataValue, the nodata value should be an integer
  noDataKey: undefined,

  // The block size to use for buffer
  blockSize: 65536,

  // Optional, override default opacity of 1 on the image added to the map
  opacity: 1,
};
const tiffurl = "http://127.0.0.1:5500/data/norm.tif";

var layer = L.leafletGeotiff(tiffurl, options).addTo(mymap);
console.log("okpopo");

/*const file = geoTIFF.fromFile(tiffurl);
const image = file.getImage();
const bbox = image.getBoundingBox();
console.log(bbox);
*/
