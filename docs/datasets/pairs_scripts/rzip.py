"""Read members of a remote zip via explicit HTTP Range requests."""
import io, sys, zipfile, requests

class RangeFile(io.RawIOBase):
    def __init__(self, url: str, size: int) -> None:
        self.url, self.size, self.pos = url, size, 0
        self.s = requests.Session()
    def seekable(self) -> bool: return True
    def readable(self) -> bool: return True
    def tell(self) -> int: return self.pos
    def seek(self, off: int, whence: int = 0) -> int:
        self.pos = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off)
        return self.pos
    def read(self, n: int = -1) -> bytes:
        if n is None or n < 0: n = self.size - self.pos
        if n == 0 or self.pos >= self.size: return b""
        end = min(self.pos + n, self.size) - 1
        r = self.s.get(self.url, headers={"Range": f"bytes={self.pos}-{end}"}, timeout=120)
        r.raise_for_status()
        self.pos += len(r.content)
        return r.content
    def readinto(self, b):  # type: ignore[override]
        d = self.read(len(b)); b[:len(d)] = d; return len(d)

def open_remote(url: str) -> zipfile.ZipFile:
    h = requests.head(url, allow_redirects=True, timeout=60)
    size = int(h.headers["content-length"])
    return zipfile.ZipFile(io.BufferedReader(RangeFile(h.url, size), buffer_size=1 << 20))

if __name__ == "__main__":
    url, *members = sys.argv[1:]
    z = open_remote(url)
    if members and members[0] == "--peek":
        print(z.open(members[1]).read(int(members[2])).decode("utf-8", "replace")); sys.exit()
    if members and members[0] == "--raw":
        # copy one member decompressed to a local path, streaming
        with z.open(members[1]) as src, open(members[2], "wb") as dst:
            while chunk := src.read(1 << 22): dst.write(chunk)
        sys.exit()
    if not members:
        for i in z.infolist(): print(i.filename, i.file_size, i.compress_size, sep="\t")
    else:
        out = members.pop()
        for m in members: z.extract(m, out)
