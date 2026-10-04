"""Serve local replay files with HTTP byte ranges for video seeking.

영상의 필요한 바이트 구간만 응답하여 랩 이동과 재생 탐색을 지원합니다.
Run from any directory: python src/serve_replays.py --port 8767
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]


class ReplayHandler(SimpleHTTPRequestHandler):
    """Support one byte range per request; bind to localhost by default."""

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        super().end_headers()

    def send_head(self):
        self.bytes_remaining = None
        requested = self.headers.get('Range')
        path = Path(self.translate_path(self.path))
        if not requested or not path.is_file():
            return super().send_head()
        size = path.stat().st_size
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', requested.strip())
        start, end = 0, size - 1
        valid = bool(match and size > 0)
        if valid:
            first, last = match.groups()
            if not first and not last:
                valid = False
            elif not first:
                valid = int(last) > 0
                start = max(0, size-int(last))
            else:
                start = int(first)
                end = min(int(last), size-1) if last else size-1
                valid = 0 <= start <= end < size
        if not valid:
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        stream = path.open('rb')
        stream.seek(start)
        self.bytes_remaining = end-start+1
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(self.bytes_remaining))
        self.send_header('Last-Modified', self.date_time_string(path.stat().st_mtime))
        self.end_headers()
        return stream

    def copyfile(self, source, outputfile):
        try:
            self.copy_requested_bytes(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            # Browsers cancel old ranges when seeking; this is expected.
            pass

    def copy_requested_bytes(self, source, outputfile):
        if self.bytes_remaining is None:
            return super().copyfile(source, outputfile)
        remaining = self.bytes_remaining
        while remaining:
            block = source.read(min(65536, remaining))
            if not block:
                break
            outputfile.write(block)
            remaining -= len(block)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8767)
    args = parser.parse_args()
    def handler(*arguments, **keywords):
        return ReplayHandler(*arguments, directory=str(ROOT), **keywords)
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    print(f'http://127.0.0.1:{args.port}/outputs/ko/v4/replay.html', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
