"""Deferred TCP reads must outlive response, header and handshake buffers."""
import unittest
from response_harness import method, run_cases

SOURCE = r"""
#include "response_fixture.h"
#include <cstdlib>
struct AsyncBasicResponse {
  size_t _ackedLength=0, _writtenLength=0, _writtenHeadersLength=0, _sentLength=0;
  int _state=RESPONSE_HEADERS;
  String _assembled_headers, _content;
  size_t write_send_buffs(AsyncWebServerRequest *, size_t, uint32_t);
};
namespace asyncsrv { const char *T_HTTP_503_HEAD="503"; }
const char *T_Last_Event_ID="Last-Event-ID";
const std::string head="HTTP/1.1 200 OK\r\nX-Long-Header: " + std::string(96, 'h') + "\r\n\r\n";
struct AsyncWebSocketResponse {
  int _state=RESPONSE_SETUP;
  size_t _headLength=0;
  AsyncWebServerRequest *_request=nullptr;
  bool _sourceValid() const {return true;}
  bool _assembleHead(String &out, unsigned) {out=head;_headLength=out.size();return true;}
  void _switchClient() {}
  void _respond(AsyncWebServerRequest *);
};
struct AsyncEventSourceClient {
  static std::vector<AsyncEventSourceClient *> instances;
  AsyncEventSourceClient(Client *, void *, uint32_t) {instances.push_back(this);}
};
std::vector<AsyncEventSourceClient *> AsyncEventSourceClient::instances;
struct AsyncEventSourceResponse {
  int _state=RESPONSE_SETUP;
  size_t _headLength=0;
  void *_server=nullptr;
  bool _assembleHead(String &out, unsigned) {out=head;_headLength=out.size();return true;}
  void _respond(AsyncWebServerRequest *);
};
"""
SOURCE += "\n".join((
    method("WebResponses.cpp", "size_t AsyncBasicResponse::write_send_buffs"),
    method("WebResponses.cpp", "size_t AsyncAbstractResponse::write_send_buffs"),
    method("AsyncWebSocket.cpp", "void AsyncWebSocketResponse::_respond"),
    method("AsyncEventSource.cpp", "void AsyncEventSourceResponse::_respond"),
))
SOURCE += r"""
int main(int argc, char **argv) {
  assert(argc==2);
  const std::string scenario=argv[1];
  const std::string body(128, 'b');
  AsyncWebServerRequest request;
  request.tcp.deferred=true;
  std::string expected;
  if (scenario=="basic_header") {
    auto response=std::make_unique<AsyncBasicResponse>();
    response->_assembled_headers=head;
    response->write_send_buffs(&request,0,0);
    expected=head;
  } else if (scenario=="basic_body") {
    auto response=std::make_unique<AsyncBasicResponse>();
    response->_state=RESPONSE_CONTENT;response->_content=body;
    response->write_send_buffs(&request,0,0);
    expected=body;
  } else if (scenario=="abstract_header") {
    auto response=std::make_unique<AsyncAbstractResponse>();
    response->_state=RESPONSE_HEADERS;response->_assembled_headers=head;
    response->write_send_buffs(&request,0,0);
    expected=head;
  } else if (scenario=="abstract_body") {
    auto response=std::make_unique<AsyncAbstractResponse>();
    response->_send_buffer=std::make_unique<std::array<uint8_t,ASYNC_RESPONCE_BUFF_SIZE>>();
    memcpy(response->_send_buffer->data(),body.data(),body.size());
    response->_send_buffer_len=body.size();
    response->write_send_buffs(&request,0,0);
    expected=body;
  } else if (scenario=="websocket") {
    AsyncWebSocketResponse response;response._respond(&request);expected=head;
  } else if (scenario=="sse") {
    AsyncEventSourceResponse response;response._respond(&request);expected=head;
  } else { assert(false); }
  // Read only after the String/response callback has released its storage.
  request.tcp.flush();
  assert(request.tcp.wire==expected && !request.failures && !request.tcp.closed);
  for (auto client:AsyncEventSourceClient::instances) delete client;
}
"""


class ResponseLifetimeTests(unittest.TestCase):
    def test_deferred_reads_with_borrowing_and_copying_tcp_defaults(self):
        for flags in (0, 1):
            run_cases(self, SOURCE, ("basic_header", "basic_body", "abstract_header",
                                    "abstract_body", "websocket", "sse"),
                      ["-DASYNCWEBSERVER_USE_CHUNK_INFLIGHT=1", f"-DTEST_TCP_DEFAULT_FLAGS={flags}"])


if __name__ == "__main__":
    unittest.main()
