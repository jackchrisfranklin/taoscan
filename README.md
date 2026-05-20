# taoscan

taoscan is a simple forensic video scanner and sanitizer CLI tool.

It can scan video files for structure issues, entropy patterns, EOF problems, and suspicious data. It can also rebuild or sanitize files if needed.

---

## install

from source:

```bash
git clone https://github.com/jackhession/taoscan.git
cd taoscan
pip install -r requirements.txt
```

or install the latest `.deb` from the releases page:

👉 https://github.com/jackhession/taoscan/releases

then:

sudo dpkg -i taoscan_version_amd64.deb

---

## usage

basic scan:

```
taoscan video.mp4
```

---

## scan options

```
taoscan video.mp4 --score --entropy --structure --eof
```

--score        anomaly score
--entropy      entropy checks
--structure    file/container structure checks
--eof          eof / truncation check

---

## interpret results

```
taoscan video.mp4 --interpret
```

prints a simple interpretation of the scan results

---

## sanitize / rebuild

sanitize file:

```
taoscan video.mp4 --sanitize --out clean.mp4
```

rebuild (re-encode):

```
taoscan video.mp4 --rebuild --out rebuilt.mp4
```

extract suspicious data:

```
taoscan video.mp4 --extract
```

---

## combined example

```
taoscan video.mp4 --score --entropy --interpret --sanitize --out clean.mp4
```

---

## output

everything outputs json to the terminal

---

## notes

- built for quick forensic checks on video files
- works best with standard video formats
- can be used in scripts since output is json
- project released under Apache 2.0 license
