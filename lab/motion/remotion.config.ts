/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// H.264 MP4 for YouTube: visually lossless, tagged BT.709 so colours match the Studio preview.
Config.setCodec("h264");
Config.setCrf(18);
Config.setColorSpace("bt709");
