# ESPAsyncWebServer

This integration branch combines the independent upstream fixes in [PR #509](https://github.com/ESP32Async/ESPAsyncWebServer/pull/509) (partial-write accounting) and [PR #510](https://github.com/ESP32Async/ESPAsyncWebServer/pull/510) (temporary buffer lifetime), plus an ESP8266 header-allocation memory guard. The upstream PR branches remain separate.

The ESP8266 dependency is pinned to the minimal [labodj/ESPAsyncTCP](https://github.com/labodj/ESPAsyncTCP) fork. Other architectures keep their upstream TCP dependencies. Pin this branch to a full commit SHA in firmware; `3.12.1-labo.1` identifies this fork and is not an upstream release. Arduino IDE users must install the TCP fork separately.

Native regressions run with GCC/Clang, AddressSanitizer and UBSan: `python3 -m unittest discover -s tests -v`. Upstream API documentation and notices follow below.

![https://avatars.githubusercontent.com/u/195753706?s=96&v=4](https://avatars.githubusercontent.com/u/195753706?s=96&v=4)

[![Latest Release](https://img.shields.io/github/release/ESP32Async/ESPAsyncWebServer.svg)](https://GitHub.com/ESP32Async/ESPAsyncWebServer/releases/)
[![PlatformIO Registry](https://badges.registry.platformio.org/packages/ESP32Async/library/ESPAsyncWebServer.svg)](https://registry.platformio.org/libraries/ESP32Async/ESPAsyncWebServer)

[![License: LGPL 3.0](https://img.shields.io/badge/License-LGPL%203.0-yellow.svg)](https://opensource.org/license/lgpl-3-0/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](docs/code_of_conduct.md)

[![GitHub latest commit](https://badgen.net/github/last-commit/ESP32Async/ESPAsyncWebServer)](https://GitHub.com/ESP32Async/ESPAsyncWebServer/commit/)

[![Documentation](https://img.shields.io/badge/Documentation-Visit%20Site-blue?logo=materialformkdocs)](https://esp32async.github.io/ESPAsyncWebServer/)

## 📚 Documentation

**[Read the Full Documentation Here 📖](https://ESP32Async.github.io/ESPAsyncWebServer/)**

The documentation has been moved to a dedicated website to provide a better reading experience.

## Overview

Asynchronous HTTP and WebSocket Server Library for ESP32, ESP8266, RP2040, and RP2350.

**Key Features:**

- **Asynchronous**: Handle multiple connections simultaneously.
- **Fast**: Optimized for performance.
- **WebSockets**: Built-in support for real-time communication.
- **SSE**: Server-Sent Events support.
- **Middleware**: Flexible request processing (Authentication, CORS, Rate Limiting, etc.).
- **File Serving**: Static file serving, File Uploads.
- **Templating**: Simple template processing.
- **Json & MessagePack**: Native support.
- **Routing**: Powerful URL matching (Exact, Prefix, Regex, etc.).

## Compatibility

- **Chips**: ESP32, ESP8266, RP2040, RP2350
- **Frameworks**: Arduino Core 2.x and 3.x, PlatformIO

## License

This project is licensed under the LGPL-3.0 License - see the [LICENSE](LICENSE) file for details.
